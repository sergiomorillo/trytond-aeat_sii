# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from . import aeat

__all__ = ['Party', 'PartyIdentifier']


class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta

    sii_identifier_type = fields.Selection(aeat.PARTY_IDENTIFIER_TYPE,
        'SII Identifier Type', sort=False)
    sii_vat_code = fields.Function(fields.Char('SII VAT Code', size=9),
        'get_sii_vat_data')
    sii_vat_country = fields.Function(fields.Char('SII VAT Country', size=2),
        'get_sii_vat_data')

    def get_sii_vat_data(self, name=None):
        vat_code = self.vat_code
        if vat_code:
            type = None
            for identifier in self.identifiers:
                if identifier.code == vat_code:
                    type = identifier.type
                    break
            if name == 'sii_vat_code':
                return vat_code[2:] if type == 'eu_vat' else vat_code
            elif name == 'sii_vat_country':
                return vat_code[:2] if type == 'eu_vat' else None


class PartyIdentifier:
    __metaclass__ = PoolMeta
    __name__ = 'party.identifier'

    @classmethod
    def set_sii_identifier_type(cls, identifiers):
        Party = Pool().get('party.party')

        to_write = []
        for identifier in identifiers:
            write = True
            type_ = identifier.type
            if type_ == 'eu_vat':
                if identifier.code.startswith('ES'):
                    sii_identifier_type = None
                else:
                    sii_identifier_type = '02'
            elif type_ == 'eu_not_vat':
                sii_identifier_type = '04'
            else:
                write = False

            if write:
                to_write.extend(([identifier.party], {
                    'sii_identifier_type': sii_identifier_type}))

        if to_write:
            Party.write(*to_write)

    @classmethod
    def create(cls, vlist):
        identifiers = super(PartyIdentifier, cls).create(vlist)
        cls.set_sii_identifier_type(identifiers)
        return identifiers

    @classmethod
    def write(cls, *args):
        super(PartyIdentifier, cls).write(*args)

        def get_identifiers(identifiers):
            return list(set(identifiers))

        actions = iter(args)
        for identifiers, values in zip(actions, actions):
            cls.set_sii_identifier_type(get_identifiers(identifiers))
