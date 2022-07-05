import psycopg2
import utils_db
 
def main():
    # # execute to select row
    # utils_db.select_test_item(11)

    # # execute to insert row
    # utils_db.insert_test_item(100, "python")

    # execute to update row
    # id = 10
    # json_object = {
    #     "num" : "20",
    #     "data" : "35"
    # }
    # utils_db.update_test_item(id, json_object)

    # execute to delete row
    json_object2 = {
        "id" : "5",
        "num" : "6",
        "data" : "banana"
    }
    utils_db.delete_test_item(json_object2)
main()
