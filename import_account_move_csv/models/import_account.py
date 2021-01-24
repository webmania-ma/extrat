# -*- coding: utf-8 -*-

import base64
import csv
from odoo import models, fields
from datetime import date, datetime
from decimal import Decimal
import sys


class EcritureComptable:
    def __init__(self, row):
        for i in row.keys():
            if i == "DATE":
                j, m, a = row["DATE"].split("/")
                self.DATE = date(int(a), int(m), int(j))
            else:
                setattr(self, i, row[i])
                if i in ["DEBIT", "CREDIT"]:
                    setattr(self, i, Decimal(getattr(self, i).replace(",", ".")))


class PieceComptable:
    def __init__(self):
        self.ecritures = []

    def ajoute(self, row):
        self.JAL = row["JAL"]
        self.PCE = row["PCE"]
        ecri = EcritureComptable(row)
        self.ecritures.append(ecri)

    def estBalancee(self):
        total = Decimal(0)
        res = ""
        for e in self.ecritures:
            total += Decimal(e.DEBIT)
            total -= Decimal(e.CREDIT)
            res += " L: " + str(e.LIBELLE) + " + " + str(Decimal(e.DEBIT)) + " - " + str(Decimal(e.CREDIT))
        res += " Total: " + str(total)
        return total == Decimal(0), res


class Import_compt(models.Model):
    _name = "import_account_move_csv.import_compt"
    _description = "import_account_move_csv"

    nom = fields.Char(string="Name")
    fichier = fields.Binary(string="CSV File")
    message_erreur = fields.Text(string="Error Message", readonly="True")
    dateImport = fields.Datetime(string="Date of import", readonly="True")

    def calculeCodePiece(self, row):
        return row["JAL"] + row["PCE"]

    def importer(self, listePieces, detecteErreur=False):
        error_detected = False
        for o in listePieces:
            company = self.env.user.company_id
            j = self.env["account.journal"].search(
                [["company_id", "=", company.id], ["code", "=", o.JAL]]
            )
            if not j:
                self.message_erreur += "\nCouldn't find journal %s in company %s" % (
                    o.JAL,
                    company.name,
                )
                error_detected = True
            estBalancee, res = o.estBalancee()
            if not estBalancee:
                self.message_erreur += (
                    "\nError, account move %s %s is unbalanced: %s"
                    % (o.JAL, o.PCE, res)
                )
                error_detected = True
            if not detecteErreur:
                p = self.env["account.move"]
                piece = p.create(
                    {
                        "ref": "Import from %s" % (datetime.now()),
                        "company_id": company.id,
                        "journal_id": j.id,
                    }
                )
            for ecriture in o.ecritures:
                compte = self.env["account.account"].search(
                    [["company_id", "=", company.id], ["code", "=", ecriture.COMPTE]]
                )
                if not compte:
                    self.message_erreur += (
                        "\nCouldn't find account.account %s in company %s"
                        % (ecriture.COMPTE, company.name)
                    )
                    error_detected = True

                # find partner for account type payable or receivable
                partner_id = False
                type_receivable_id = self.env.ref(
                    "account.data_account_type_receivable"
                ).id
                type_payable_id = self.env.ref("account.data_account_type_payable").id
                account_field = False
                if compte.user_type_id.id == type_receivable_id:
                    account_field = "property_account_receivable_id"
                elif compte.user_type_id.id == type_payable_id:
                    account_field = "property_account_payable_id"
                if account_field and not compte.no_retrieve_partner:
                    res = self.env["res.partner"].search([(account_field, "=", compte.id)])
                    if not len(res):
                        self.message_erreur += (
                            "\nNo partner associated to payable/receivable account.account %s"
                            % ecriture.COMPTE
                        )
                        error_detected = True
                    elif len(res) > 1:
                        self.message_erreur += (
                            "\nMultiple partners associated to account.account %s (%s)"
                            % (ecriture.COMPTE, ", ".join(res.mapped("name")))
                        )
                        error_detected = True
                    else:
                        partner_id = res[0].id

                if not detecteErreur and not error_detected:
                    l = self.env["account.move.line"]
                    ecr = l.with_context(
                        journal_id=j,
                        check_move_validity=False,
                        line_name=ecriture.LIBELLE,
                    ).create(
                        {
                            "account_id": compte.id,
                            "date": ecriture.DATE,
                            "debit": ecriture.DEBIT,
                            "credit": ecriture.CREDIT,
                            "move_id": piece.id,
                            "journal_id": j.id,
                            "date_maturity": ecriture.DATE,
                            "name": ecriture.LIBELLE,
                            "partner_id": partner_id,
                        }
                    )
        return not error_detected

    def importer_fichier(self):
        self.ensure_one()
        try:
            decode = base64.b64decode(self.fichier).decode("utf-8")
            reader = csv.DictReader(decode.splitlines(), delimiter=",", quotechar='"')
            piecesParCode = {}
            for row in reader:
                piecesParCode.setdefault(
                    self.calculeCodePiece(row), PieceComptable()
                ).ajoute(row)
        except:
            self.message_erreur = (
                str(sys.exc_info()[0])
                + " Error while reading CSV file. Are the columns DATE	JAL	COMPTE	PCE	LIBELLE	DEBIT	CREDIT \n "
                " Is the file comma separated, and the delimiter the double quote? no blank field?"
            )
            return

        self.message_erreur = "Error:"
        list_pieces = piecesParCode.values()
        list_pieces = sorted(list_pieces, key=lambda piece: piece.ecritures[0].DATE)
        if not self.importer(list_pieces, detecteErreur=True):
            return False
        if self.importer(list_pieces):
            self.message_erreur = "IMPORT OK"
            self.dateImport = datetime.now()
        return self
