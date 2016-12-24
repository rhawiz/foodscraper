MAX_ID = 100212
URL_FORMAT = "http://nutritiondata.self.com/foods-{cat_id}000000000000000000.html"

categories = ["020",
              "008",
              "018",
              "011",
              "009",
              "012",
              "016",
              "015",
              "005",
              "013",
              "010",
              "017",
              "007",
              "001",
              "006",
              "004",
              "023",
              "019",
              "002",
              "014",
              "003",
              "043",
              "022"]

fields = {
    "name": "facts-heading",
    "calories_total": "",
    "carbohydrate_total": "",
    "carbohydrate_fiber": "",
    "carbohydrate_starch": "",
    "carbohydrate_sugar": "",
    "protein_total": "",
    "fat_total": "",
    "fat_saturated": "",
    "fat_monosaturated": "",
    "fat_polysaturated": "",
    "minerals_calcium": "",
    "minerals_iron": "",
    "minerals_magnesium": "",
    "minerals_phosphorus": "",
    "minerals_sodium": "",
    "minerals_zinc": "",
    "minerals_copper": "",
    "minerals_manganese": "",
    "minerals_selenium": "",
    "minerals_fluoride": "",
    "vitamins_a": "",
    "vitamins_c": "",
    "vitamins_d": "",
    "vitamins_e": "",
    "vitamins_k": "",
    "vitamins_thiamin": "",
    "vitamins_riboflavin": "",
    "vitamins_niacin": "",
    "vitamins_b6": "",
    "vitamins_folate": "",
    "vitamins_b12": "",
    "vitamins_choline": "",
    "vitamins_betaine": "",
    "sterols_cholestrol": "",
    "other_alcohol": "",
    "other_water": "",
    "other_caffeine": "",
}



if __name__ == "__main__":
    for cat_id in categories:
        url = construct_url(URL_FORMAT, cat_id)

        print url
