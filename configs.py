# -*- coding: utf-8 -*-

"""
Scrape information contained here with the following structure



"""

SOURCES_CONFIGS = {
    "nutritiondata": {
        "name": "nutritiondata",
        "domain": "http://nutritiondata.self.com/",
        "detail_info": {
            "save_html": True,
            "save_url_info": True,
            "javascript": True,
            "javascript_calls": [],
            "unit_container": [
                ("div", {"class": "analysis-content-wrap"})
            ],
            "fields": {
                "name": {
                    "tags": [
                        ("div", {"class": "facts-heading"}),
                        ("", "")
                    ],
                    "replace": [
                        (' +', ' '),
                        ('', '')
                    ]
                },
                "serving_options": {
                    "tags": [
                        ("select", {"name": "serving"}),
                        ("", "")
                    ],
                    "replace": [
                        ('\n', ','),
                        ('^\,', ''),
                        ('\,$', ''),
                    ]
                },
                "calories_total": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_0"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", ""),
                        ("", ""),
                        (' +', ' '),

                    ]
                },
                "carbohydrate_fiber": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_5"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", ""),
                        ("", ""),
                        (' +', ' '),

                    ]
                },
                "carbohydrate_starch": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_6"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", "0"),
                        (' +', ' '),
                        ("", ""),

                    ]
                },
                "carbohydrate_sugar": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_7"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", "0"),
                        (' +', ' '),
                        ("", ""),

                    ]
                },
                "protein_total": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_77"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", "0"),
                        (' +', ' '),
                        ("", ""),

                    ]
                },
                "fat_total": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_14"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", "0"),
                        (' +', ' '),
                        ("", ""),

                    ]
                },
                "fat_saturated": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_15"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", "0"),
                        (' +', ' '),
                        ("", ""),

                    ]
                },
                "fat_monosaturated": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_31"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", "0"),
                        (' +', ' '),
                        ("", ""),

                    ]
                },
                "fat_polysaturated": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_46"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", "0"),
                        (' +', ' '),
                        ("", ""),

                    ]
                },
                "minerals_calcium": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_117"}),
                        ("", ""),
                    ],
                    "replace": [
                        ("\~", "0"),
                        (' +', ' '),
                        ("", ""),

                    ]
                }, "minerals_iron": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_118"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "minerals_magnesium": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_119"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "minerals_phosphorus": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_120"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "minerals_potassium": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_121"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "minerals_sodium": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_122"}),
                        ("", "")
                    ], "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "minerals_zinc": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_123"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "minerals_copper": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_124"}),
                        ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "minerals_manganese": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_125"}),
                        ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "minerals_selenium_mcg": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_126"}),
                        ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "minerals_fluoride": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_145"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_a": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_97"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_c": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_100"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_d": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_101"}),
                        ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_e": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_102"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_k": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_103"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_thiamin": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_107"}),
                        ("", "")
                    ],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_riboflavin": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_108"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_niacin": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_109"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]},
                "vitamins_b6": {
                    "tags":
                        [
                            ("span", {"id": "NUTRIENT_110"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_folate": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_111"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_b12": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_115"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "pantothenic_acid": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_116"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_choline": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_143"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "vitamins_betaine": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_144"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "sterols_cholestrol": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_72"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "other_alcohol": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_127"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "other_water": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_128"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
                "other_caffeine": {
                    "tags": [
                        ("span", {"id": "NUTRIENT_130x`"}), ("", "")],
                    "replace": [
                        ("~", "0"),
                        (' +', ' '),
                        ("", ""),
                    ]
                },
            }
        },

        "listing_info": {
            "url_prefix": "http://nutritiondata.self.com",
            "javascript": True,
            "javascript_calls": [],
            "details_url": [
                ("td", {"class": "note2"}),
                ("a", {"class": "list"}),
                ("", "href"),
            ],
            "replace": [
                ("\/2", "/0")
            ],

            "next_page": [
                ("a", {"title": "Next"}),
                ("", "href"),
                ("regex", "\/foods\-[0-9]+?\-[0-9]\.html\?"),
            ]
        },
        "url_info": {
            "format": "http://nutritiondata.self.com/foods-{category}000000000000000000.html",
            "params": {
                "category": [
                    "020",
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
            }
        }
    }

}
