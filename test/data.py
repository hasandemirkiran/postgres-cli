import pprint

ortho_last_dic = {'ArenbergMeppen': {'Eleonorenwald': ['/Volumes/gis_data/customers/ArenbergMeppen/Eleonorenwald/raster/Orthos/Ortho__Eleonorenwald_801_836__75mm__1200mm__2020_06_24.gpkg',
                                      '/Volumes/gis_data/customers/ArenbergMeppen/Eleonorenwald/raster/Orthos/Ortho__Eleonorenwald_851_857__80mm__1280mm__2020_06_24.gpkg'],
                    'Engelbertswald': ['/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_101_106__66mm__1005mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_101_106__66mm__264mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_121_125__65mm__1005mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_121_125__65mm__262mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_131__79mm__1264mm__2020_06_24.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_141_142__73mm__1168mm__2020_06_24.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_151_164__65mm__1005mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_151_164__65mm__262mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_171_173__66mm__1006mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_171_173__66mm__265mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_181__64mm__1020mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_181__64mm__255mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_191_201__64mm__1030mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_191_201__64mm__256mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_220_230__64mm__1003mm__2020_08_06.gpkg',
                                       '/Volumes/gis_data/customers/ArenbergMeppen/Engelbertswald/raster/Orthos/Ortho__Engelbertswald_220_230__64mm__257mm__2020_08_06.gpkg'],
                    'Hedwigenwald': ['/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_601__76mm__1216mm__2020_06_24.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_611_626__64mm__1003mm__2020_08_06.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_611_626__64mm__264mm__2020_08_06.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_631_647__80mm__1280mm__2020_06_24.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_661__61mm__123mm__2020_10_23.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_661__61mm__984mm__2020_10_23.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_681__63mm__1010mm__2020_10_23.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_681__63mm__126mm__2020_10_23.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_691__63mm__1014mm__2020_10_23.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_691__63mm__127mm__2020_10_23.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_701_703__66mm__1058mm__2020_10_26.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_701_703__66mm__132mm__2020_10_26.gpkg',
                                     '/Volumes/gis_data/customers/ArenbergMeppen/Hedwigenwald/raster/Orthos/Ortho__Hedwigenwald_711_720__80mm__1280mm__2020_06_24.gpkg'],
                    'Karlswald': ['/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_301__65mm__1037mm__2020_10_26.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_301__65mm__130mm__2020_10_26.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_311_323__65mm__1037mm__2020_10_26.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_311_323__65mm__130mm__2020_10_26.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_331__62mm__1000mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_331__62mm__125mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_341__82mm__1312mm__2020_06_24.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_351_354__63mm__1010mm__2020_08_06.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_351_354__63mm__253mm__2020_08_06.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_371_384__65mm__1004mm__2020_08_06.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_371_384__65mm__261mm__2020_08_06.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_401_422__64mm__1022mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_401_422__64mm__128mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_431_435__70mm__1114mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_431_435__70mm__139mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_441_442__67mm__1068mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_441_442__67mm__133mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_453_451__67mm__1068mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_453_451__67mm__134mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_461_471__77mm__1232mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_461_471__77mm__154mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_491_495__69mm__1102mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_491_495__69mm__138mm__2020_10_23.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_501_506__82mm__1312mm__2020_06_24.gpkg',
                                  '/Volumes/gis_data/customers/ArenbergMeppen/Karlswald/raster/Orthos/Ortho__Meyerei_511_513__82mm__1312mm__2020_06_24.gpkg']},
 'Blauwald': {'Duttenstein': ['/Volumes/gis_data/customers/Blauwald/Duttenstein/raster/Orthos/Ortho__Duttenstein__66mm__1050mm__2021_06_14.gpkg'],
              'Ebnat': ['/Volumes/gis_data/customers/Blauwald/Ebnat/raster/Orthos/Ortho__Ebnat_0__65mm__1040mm__2020_07_20.gpkg',
                        '/Volumes/gis_data/customers/Blauwald/Ebnat/raster/Orthos/Ortho__Ebnat_1__65mm__1040mm__2020_07_20.gpkg',
                        '/Volumes/gis_data/customers/Blauwald/Ebnat/raster/Orthos/Ortho__Ebnat_2__65mm__1040mm__2020_07_20.gpkg',
                        '/Volumes/gis_data/customers/Blauwald/Ebnat/raster/Orthos/Ortho__Ebnat_3__65mm__1040mm__2020_07_20.gpkg']},
 'CenterForst': {'Baumbach': ['/Volumes/gis_data/customers/CenterForst/Baumbach/raster/Orthos/Ortho__Baumbach__76mm__2021_03_30.gpkg',
                              '/Volumes/gis_data/customers/CenterForst/Baumbach/raster/Orthos/Ortho__Baumbach__76mm__2021_03_30__CIR.gpkg'],
                 'Immergruen': ['/Volumes/gis_data/customers/CenterForst/Immergruen/raster/Orthos/Ortho__Immergruen__48mm__774mm__2021_08_27.gpkg'],
                 'Weide': ['/Volumes/gis_data/customers/CenterForst/Weide/raster/Orthos/Ortho__Weide__48mm__774mm__2021_08_27.gpkg']},
 'DeutscheBahn': {'DeutscheBahn': ['/Volumes/gis_data/customers/DeutscheBahn/raster/Ortho__Mühldorf__25mm__155mm__2020_05_27.gpkg']},
 'Fugger': {'Wellenburg': ['/Volumes/gis_data/customers/Fugger/Wellenburg/raster/Ortho__Wellenburg__63mm__1010mm__2021_02_20.gpkg',
                           '/Volumes/gis_data/customers/Fugger/Wellenburg/raster/Orthos/Ortho__Wellenburg__63mm__1010mm__2021_02_20.gpkg']},
 'GrafSpreti': {'Lotzbeck': ['/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/raster/Orthos/Ortho__Lotzbeck_1__66mm__1063mm__2021_09_24.gpkg',
                             '/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/raster/Orthos/Ortho__Lotzbeck_2__65mm__1046mm__2021_09_24.gpkg',
                             '/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/raster/Orthos/Ortho__Lotzbeck_3__65mm__1046mm__2021_09_24.gpkg',
                             '/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/raster/Orthos/Ortho__Lotzbeck_4__66mm__1056mm__2021_09_24.gpkg',
                             '/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/raster/Orthos/before_color_correction/Ortho__Lotzbeck_1__66mm__1063mm__2021_09_24.gpkg',
                             '/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/raster/Orthos/before_color_correction/Ortho__Lotzbeck_2__65mm__1046mm__2021_09_24.gpkg',
                             '/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/raster/Orthos/before_color_correction/Ortho__Lotzbeck_3__65mm__1046mm__2021_09_24.gpkg',
                             '/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/raster/Orthos/before_color_correction/Ortho__Lotzbeck_4__66mm__1056mm__2021_09_24.gpkg']},
 'HofosOldershausen': {'Breitenbach': ['/Volumes/gis_data/customers/HofosOldershausen/Breitenbach/raster/Orthos/Ortho__Breitenbach__55mm__881mm__2021_08_30.gpkg'],
                       'Fienerode': ['/Volumes/gis_data/customers/HofosOldershausen/Fienerode/raster/Orthos/Ortho__Fienerode__72mm__1160mm__2020_06_23.gpkg',
                                     '/Volumes/gis_data/customers/HofosOldershausen/Fienerode/raster/Orthos/Ortho__Fienerode__72mm__145mm__2020_06_23.gpkg',
                                     '/Volumes/gis_data/customers/HofosOldershausen/Fienerode/raster/Orthos/Ortho__Fienerode__95mm__1160mm__2020_01_17.gpkg'],
                       'Muenzenberg': ['/Volumes/gis_data/customers/HofosOldershausen/Muenzenberg/raster/Orthos/Ortho__Muenzenberg__76mm__2021_03_30.gpkg']},
 'ToeringJettenbach': {'Duenzelbach': ['/Volumes/gis_data/customers/ToeringJettenbach/Duenzelbach/raster/Orthos/Ortho__Dunzelbach__63mm__1010mm__2021_02_20.gpkg',
                                       '/Volumes/gis_data/customers/ToeringJettenbach/Duenzelbach/raster/Orthos/Ortho__Dunzelbach__63mm__1010mm__2021_02_20_wg84_gdal.gpkg',
                                       '/Volumes/gis_data/customers/ToeringJettenbach/Duenzelbach/raster/Orthos/Ortho__Dunzelbach__63mm__1010mm__2021_02_20_wg84_qgis.gpkg'],
                       'Gutenzell': ['/Volumes/gis_data/customers/ToeringJettenbach/Gutenzell/raster/Orthos/Ortho__Gutenzell-0__62mm__246mm__2020_07_13.gpkg',
                                     '/Volumes/gis_data/customers/ToeringJettenbach/Gutenzell/raster/Orthos/Ortho__Gutenzell-1__62mm__246mm__2020_07_13.gpkg'],
                       'Inning': ['/Volumes/gis_data/customers/ToeringJettenbach/Inning/raster/Orthos/Ortho__Inning_3__69mm__1100mm__2021_02_14.gpkg',
                                  '/Volumes/gis_data/customers/ToeringJettenbach/Inning/raster/Orthos/Ortho__Seefeld_Inning_2__66mm__1060mm__2021_02_14.gpkg',
                                  '/Volumes/gis_data/customers/ToeringJettenbach/Inning/raster/Orthos/Ortho__Seefeld_Inning_2__66mm__528mm__2021_02_14.gpkg'],
                       'Jettenbach': ['/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/raster/Orthos/Ortho__Jettenbach_12__62mm__995mm__2021_06_14.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/raster/Orthos/Ortho__Jettenbach_13__65mm__1040mm__2021_06_14.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/raster/Orthos/Ortho__Jettenbach_14__54mm__867mm__2021_07_23.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/raster/Orthos/Ortho__Jettenbach_1__66mm__1060mm__2021_06_14.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/raster/Orthos/Ortho__Jettenbach_3__69mm__1100mm__2021_06_14.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/raster/Orthos/Ortho__Jettenbach_5__58mm__932mm__2021_07_23.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/raster/Orthos/Ortho__Jettenbach_7__58mm__932mm__2021_07_23.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/raster/Orthos/Ortho__Jettenbach_8__88mm__1060mm__2021_06_14.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/raster/Orthos/Ortho__Jettenbach_9__65mm__1040mm__2021_06_14.gpkg'],
                       'Mischenried': ['/Volumes/gis_data/customers/ToeringJettenbach/Mischenried/raster/Orthos/Ortho__Mischenried_1__63mm__1010mm__2021_02_14.gpkg'],
                       'Seefeld': ['/Volumes/gis_data/customers/ToeringJettenbach/Seefeld/raster/Orthos/Ortho__SeefeldInning_2__66mm__1060mm__2021_02_14.gpkg',
                                   '/Volumes/gis_data/customers/ToeringJettenbach/Seefeld/raster/Orthos/Ortho__SeefeldInning_2__66mm__528mm__2021_02_14.gpkg'],
                       'Winhoering': ['/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/raster/Orthos/Ortho__Winhoering_1__59mm__948mm__2021_07_23.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/raster/Orthos/Ortho__Winhoering_2__61mm__973mm__2021_07_23.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/raster/Orthos/Ortho__Winhoering_3__60mm__967mm__2021_07_23.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/raster/Orthos/Ortho__Winhoering_3__73mm__1160mm__2021_03_01.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/raster/Orthos/Ortho__Winhoering_4__67mm__1080mm__2021_07_23.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/raster/Orthos/Ortho__Winhoering_5__67mm__1080mm__2021_07_23.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/raster/Orthos/Ortho__Winhoering_6__65mm__1030mm__2021_07_23.gpkg',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/raster/Orthos/Ortho__Winhoering_7__57mm__908mm__2021_07_23.gpkg']},
 'VonPfuel': {'Tuessling': ['/Volumes/gis_data/customers/VonPfuel/Tuessling/raster/Orthos/Ortho__Tuessling_1__66mm__1050mm__2021_07_23.gpkg',
                            '/Volumes/gis_data/customers/VonPfuel/Tuessling/raster/Orthos/Ortho__Tuessling_2__61mm__484mm__2021_07_23.gpkg',
                            '/Volumes/gis_data/customers/VonPfuel/Tuessling/raster/Orthos/Ortho__Tuessling_3__61mm__484mm__2021_07_23.gpkg',
                            '/Volumes/gis_data/customers/VonPfuel/Tuessling/raster/Orthos/Ortho__Tuessling_4__65mm__1040mm__2021_07_23.gpkg',
                            '/Volumes/gis_data/customers/VonPfuel/Tuessling/raster/Orthos/Ortho__Tuessling_5__65mm__1040mm__2021_07_23.gpkg']},
 'Wallerstein': {'Dist_12_13': ['/Volumes/gis_data/customers/Wallerstein/Dist_12_13/raster/Orthos/Ortho__Dist_12_13__67mm__1070mm__2021_06_14.gpkg',
                                '/Volumes/gis_data/customers/Wallerstein/Dist_12_13/raster/Orthos/Ortho__Dist_12_13__68mm__1090mm__2021_03_01.gpkg'],
                 'Dist_30_31': ['/Volumes/gis_data/customers/Wallerstein/Dist_30_31/raster/Orthos/Ortho__Dist_30_31__65mm__270mm.gpkg',
                                '/Volumes/gis_data/customers/Wallerstein/Dist_30_31/raster/Orthos/Ortho__Dist_30_31__65mm__310mm__2020_07_31.gpkg']}}


# ortho_info_list = [] 

# for customer in ortho_last_dic:
#     for region in ortho_last_dic[customer]:
#         for url in list(ortho_last_dic[customer][region]):
#             x = url.split('/')
#             y = x[-1].split('__')
#             region_part = y[1]
#             if len(y) == 5 and y[-1] != 'CIR.gpkg':
#                 gsd = y[2]
#                 resolution = y[3]
#                 date = y[4].split('.')[0]
#             else:
#                 if int(y[2][:-2]) < 100:
#                     gsd = y[2]
#                     resolution = -1
#                 else:
#                     gsd = -1
#                     resolution = y[2]

#                 date = y[3].split('.')[0]
#             extn = x[-1].split('.')[-1]


#             info = {
#                 'customer' : customer, 
#                 'region' : region,
#                 'region_part' : region_part,
#                 'gsd' : gsd,
#                 'resolution' : resolution,
#                 'date' : date,
#                 'extn' : extn
#             }
#             ortho_info_list.append(info)


# pprint.pprint(ortho_info_list)

            # print(x)
            # print(y)

                
# pprint.pprint(ortho_last_dic)




label_last_dict = {'Blauwald': {'Duttenstein': ['/Volumes/gis_data/customers/Blauwald/Duttenstein/image_processing_data/labels/Label__Duttenstein__david__v1.geojson',
                              '/Volumes/gis_data/customers/Blauwald/Duttenstein/image_processing_data/labels/Label__Duttenstein__felix__v1.geojson',
                              '/Volumes/gis_data/customers/Blauwald/Duttenstein/image_processing_data/labels/Label__Duttenstein__sarah__v1.geojson']},
 'Fugger': {'Wellenburg': ['/Volumes/gis_data/customers/Fugger/Wellenburg/image_processing_data/labels/Label__Wellenburg__incl_fir__v2.geojson',
                           '/Volumes/gis_data/customers/Fugger/Wellenburg/image_processing_data/labels/Label__Wellenburg__v2.geojson']},
 'GrafSpreti': {'Lotzbeck': ['/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/image_processing_data/labels/Label__Lotzbeck_1__luca__v1.geojson',
                             '/Volumes/gis_data/customers/GrafSpreti/Lotzbeck/image_processing_data/labels/Label__Lotzbeck_4__hasan__v1.geojson']},
 'ToeringJettenbach': {'Jettenbach': ['/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_12__2021_08_02-07_19_122__v1.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_12__2021_08_02-07_19_122__v2.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_12__2021_08_02-07_19_122__v3.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_14__54mm__867mm__2021_08_24-11_47_48__v2.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_1__2021_08_02-07_21_17__v1.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_1__2021_08_02-07_21_17__v2.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_3__2021_08_02-07_18_55__v1.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_3__2021_08_02-07_18_55__v2.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_3__2021_08_02-07_18_55__v3.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_5__58mm__932mm__2021_08_24-11_45_44__v2.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_7__58mm__932mm__2021_08_24-11_46_49__v2.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_8__2021_08_04-08_51_43__v1.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Jettenbach/image_processing_data/labels/Label__Jettenbach_8__2021_08_04-08_51_43__v2.geojson'],
                       'Winhoering': ['/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_1__Sarah__v2.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_1____v1.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_1____v4.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_2__Sarah__v2.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_2____v1.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_2____v4.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_3__SarahChristian__v3.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/image_processing_data/labels/Label__Winhoering_3____v4.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/temp/Label__Winhoering_1____v1_raw.geojson',
                                      '/Volumes/gis_data/customers/ToeringJettenbach/Winhoering/temp/Label__Winhoering_2____v1_raw.geojson']},
 'VonPfuel': {'Tuessling': ['/Volumes/gis_data/customers/VonPfuel/Tuessling/image_processing_data/labels/Label__Tuessling_1__66mm__1050mm__2021_09_22-12_58_58.geojson',
                            '/Volumes/gis_data/customers/VonPfuel/Tuessling/image_processing_data/labels/Label__Tuessling_1__Christian__v2.geojson',
                            '/Volumes/gis_data/customers/VonPfuel/Tuessling/image_processing_data/labels/Label__Tuessling_1__Christian__v3.geojson']},
 'Wallerstein': {'Dist_12_13': ['/Volumes/gis_data/customers/Wallerstein/Dist_12_13/image_processing_data/labels/Label__Dist_12_13__winter__v2.geojson']}}

