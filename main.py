from methods import *
import threading
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

obj = Main('https://www.khanacademy.org/math/high-school-math')

page_type = obj.determinePage()

if page_type == obj.CURRICULUM:
    obj.curriculm()
    get_units = obj.getUnitsLinks()
    threads = list()

    for index in range(len(get_units)):
        unit = threading.Thread(target=obj.is_unit, args=(get_units[index],),daemon=True)
        # logging.info("unit %d : name %s.", index, get_units[index])
        unit.start()
        threads.append(unit)
        
    for index,thread in enumerate(threads):
        # logging.info("unit %d : name %s.", index, get_units[index])
        thread.join()
    
    logging.info("Total Units       %d ", obj.getUnitsLength())
    logging.info("Total Branch Len  %d ", obj.getBrancheLength())
    logging.info("total lessons     %d ", obj.getTotalLessons())
    logging.info("total branches    %s ", obj.getBranchTitles())


elif page_type == obj.BRANCH:
    obj.branch()
    get_units = obj.getUnitsLinks()

    threads = list()
    for index in range(len(get_units)):
        unit = threading.Thread(target=obj.is_unit, args=(get_units[index],),daemon=True)
        logging.info("unit %d : name %s.", index, get_units[index])
        unit.start()
        threads.append(unit)
        
    for index,thread in enumerate(threads):
        # logging.info("unit %d : name %s.", index, get_units[index])
        thread.join()
    
    logging.info("Total Units %d ", len(obj.getUnitsTitles()))
    logging.info("total lessons %d ", obj.getTotalLessons())

elif page_type == obj.UNIT:
    print('unit')
else:
    print('Cannot Determine page')

# total_units : 102 total lessons : 2353 Hight School Math ......... math1 :: 2483