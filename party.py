# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from . import aeat

__all__ = ['Party']


class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta

    sii_identifier_type = fields.Selection(aeat.PARTY_IDENTIFIER_TYPE,
        'SII Identifier Type')
