#-*-coding:utf-8-*

from obj_models import specials_default

from copy import deepcopy
from math import fabs
import res

def enter_command(obj, command, id, coord):

    obj = deepcopy(obj)
    attr = obj["model"]

    if len(command.split(" ")) == 2:

        target, value = command.split(" ")

        if target == "name":
            if value in res.images:
                attr["name"] = value
            else:
                print(" ----- ERREUR IMAGE INEXISTANTE ----- \n")
                return obj, False

        elif target == "x":
            try:
                obj["rect"] = obj["rect"].move(int(value), 0)
            except ValueError:
                print(" ----- ERREUR LA VALEUR DOIT ETRE UN ENTIER ----- \n")
                return obj, False

        elif target == "y":
            try:
                obj["rect"] = obj["rect"].move(0, int(value))
            except ValueError:
                print(" ----- ERREUR LA VALEUR DOIT ETRE UN ENTIER ----- \n")
                return obj, False

        elif target in ("pts", "p"):
            try:
                if int(value) < 0:
                    attr["pts"] = 0
                else:
                    attr["pts"] = int(value)
            except ValueError:
                print(" ----- ERREUR LA VALEUR DOIT ETRE UN ENTIER ----- \n")
                return obj, False

        elif target == "sh":
            if value == "1" or value == "0":
                attr["sh"] = int(value)
            else:
                print(" ----- ERREUR FORME INVALIDE [0/1] ----- \n")
                return obj, False

        elif target == "k1":
            if value == "1":
                attr["k"] = (True,attr["k"][1])
            elif value == "0":
                attr["k"] = (False,attr["k"][1])
            else:
                print(" ----- ERREUR PROPRIETE INVALIDE [0/1] ----- \n")
                return obj, False

        elif target == "k2":
            if value == "1":
                attr["k"] = (attr["k"][0],True)
            elif value == "0":
                attr["k"] = (attr["k"][0],False)
            else:
                print(" ----- ERREUR PROPRIETE INVALIDE [0/1] ----- \n")
                return obj, False

        elif target == "h":
            try:
                if int(value) < 0:
                    attr["h"] = -1
                else:
                    attr["h"] = int(value)
            except ValueError:
                print(" ----- ERREUR LA VALEUR DOIT ETRE UN ENTIER ----- \n")
                return obj, False

        elif target == "hb":
            try:
                value = int(value)
            except ValueError:
                print(" ----- ERREUR LA VALEUR DOIT ETRE UN NOMBRE ----- \n")
                return obj, False
            if obj["rect"].width < fabs(value) or obj["rect"].height < fabs(value):
                print(" ----- ERREUR HITBOX DISPROPORTIONEE (rect {}x{}) ----- \n".format(obj["rect"].width, obj["rect"].height))
                return obj, False
            attr["hb"] = value

        elif target == "spe":

            if len(value.split(":")) == 3:
                spe_name, spe_target, spe_value = value.split(":")
                try:
                    if attr["spe"][spe_name][spe_target]:
                        pass
                except KeyError:
                    print(" ----- ERREUR EXISTENCE ATTRIBUT SPECIAL ----- \n")
                    return obj, False
                if spe_value == "ID":
                    spe_value = "/".join(id)
                elif spe_value == "COORD":
                    spe_value = coord
                elif type(attr["spe"][spe_name][spe_target]) == bool:
                    if spe_value == "1":
                        spe_value = True
                    elif spe_value == "0":
                        spe_value = False
                else:
                    try:
                        spe_value = int(spe_value)
                    except:
                        try:
                            spe_value = float(spe_value)
                        except:
                            pass
                attr["spe"][spe_name][spe_target] = spe_value
            else:
                print(" ----- ERREUR SYNTAXE SPECIAL ----- \n")
                return obj, False

        elif target == "rect":

            try:
                obj["rect"].size = int(value.split("*")[0]), int(value.split("*")[1])
            except:
                print(" ----- ERREUR VALEUR ----- \n")
                return obj, False

        elif target == "speAdd":

            if value in specials_default:
                attr["spe"][value] = specials_default[value]
            else:
                print(" ----- ERREUR SPECIAL INNEXISTANT ----- \n")
                return obj, False

        else:

            print(" ----- ERREUR COMMANDE INCONNUE ----- \n")
            return obj, False

    elif len(command.split(" ")) == 1 and "!" in command:

        if command == "solid!":
            attr["k"] = (True,attr["k"][1])
        elif command == "unsolid!":
            attr["k"] = (False,attr["k"][1])
        elif command == "hazard!":
            attr["k"] = (attr["k"][0],True)
        elif command == "unhazard!":
            attr["k"] = (attr["k"][0],False)
        elif command == "rect!":
            attr["sh"] = 0
        elif command == "circle!":
            attr["sh"] = 1
        else:
            print(" ----- ERREUR COMMANDE INCONNUE ----- \n")
            return obj, False
    else:
        print(" ----- ERREUR SYNTAXE ----- \n")
        return obj, False

    obj["model"] = attr
    return obj, True
