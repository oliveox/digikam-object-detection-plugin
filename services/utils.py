from adapters import digikam
from adapters import db

class Utils:

    @classmethod
    def get_entities_to_analyse(cls):
        
        # get all internal db external image ids
        all_external_ids = db.InternalDB.get_all_external_ids()

        # get all digikam image ids
        all_image_ids = digikam.DigiKamAdapter.get_all_image_ids()

        # get list difference
        to_analyse_entity_ids = list(set(all_image_ids) - set(all_external_ids))

        # get entities to be analyzed
        to_analyse_entities = digikam.DigiKamAdapter.get_imported_entities_with_specific_ids(to_analyse_entity_ids)

        return to_analyse_entities

if __name__ == "__main__":
    result = Utils.get_entities_to_analyse()