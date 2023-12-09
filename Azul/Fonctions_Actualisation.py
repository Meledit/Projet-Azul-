from Variable import *
import os
from Fonctions_Graphique import *
from Fonctions_Initialisation import *
from Fonctions_Sauvegarde import *
from time import *
from upemtk import *
from math import *
from random import randrange
from functools import wraps
from inspect import *


######################################################################################################################
def lru_cache_possible(f):
    @wraps(f)
    def decoration(*args, **kwargs):
        # print("Appel de la fonction", str(f.__name__),":")
        arguments = signature(f).bind(*args, **kwargs).arguments
        hashable = True
        for key in arguments:
            if not arguments[key].__hash__:
                hashable = False
        # if hashable:
        #     print("\ttous les paramètres sont hashables, lru_cache est utilisable")
        # else:
        #     print("\tcertains paramètres ne sont pas hashables, lru_cache est inutilisable")
        r = f(*args, **kwargs)
        return r
    return decoration

def Choix_Nb_Joueur():
    ''' Determine le nombre de joueur, et le genre des joueurs en fonction de l'endroit où clique l'utilisateur '''
    x,y = recup_clic()
    test = 0
    if x < 6*longueur//9:
        if y < hauteur//3:
            NbJoueur = 2
            ListeTypejoueur = ['Humain','Bot']
        elif y < 2*hauteur//3:
            NbJoueur = 3
            ListeTypejoueur = ['Humain','Bot', 'Bot']
        else:
            NbJoueur = 4
            ListeTypejoueur = ['Humain','Bot','Bot','Bot']
    else:
        NbJoueur = 4
        ListeTypejoueur = ['Bot','Bot', 'Bot', 'Bot']
        test = 1
    return NbJoueur, ListeTypejoueur, test

def RemplirFabrique(NbJoueurs, Sac):
    ''' Récupère des tuiles du sac de manière aléatoire pour les mettre dans les fabriques'''
    ZoneFabrique = []
    nbTuilesDansSac = len(Sac)
    for i in range((NbJoueurs * 2) + 1):
        ZoneFabrique.append([])
        if nbTuilesDansSac<4:
            ZoneFabrique[i] = [None,None,None,None]
        else:
            for j in range(4):
                couleur = randrange(0, len(Sac))
                ZoneFabrique[i].append(Sac.pop(couleur))
                nbTuilesDansSac += -1
    return ZoneFabrique

def confirmer():
    '''Renvoie True si l'utilisateur clique à l'emplacement du bouton valider et False s'il clique à l'endroit du bouton annuler'''
    minxJ = 19 * longueur // 20                                               #Bouton jaune
    minyJ = 4 * hauteur // 15
    maxxJ = minxJ + longueur // 10
    maxyJ = 2 * minyJ

    minxR = 19 * longueur // 20
    minyR = 9 * hauteur // 15
    maxxR = minxR + longueur // 10
    maxyR = minyR + 4*hauteur//15
    while True:
        coordonee = recup_clic()
        if minxJ < coordonee[0] < maxxJ and minyJ < coordonee[1] < maxyJ:
            return True
        if minxR < coordonee[0] < maxxR and minyR < coordonee[1] < maxyR:
            return False

@lru_cache_possible
def determiner_fabrique_selectioner(coordonee, NbJoueur):
    ''' Renvoie le numero de la fabrique selectionée en fonction du nombre de fabriques totale et de l'endroit où a cliqué le joueur'''
    NbDeFabrique =(NbJoueur * 2) + 1
    if coordonee[1] < hauteur//15 +tailleC and coordonee[1] > hauteur//15 - tailleC:
        n = longueur // NbDeFabrique
        for i in range(NbDeFabrique):
            if coordonee[0] >(i*n + n//4 + tailleC - tailleC) and coordonee[0]<(i*n + n//4 + 2*tailleC):
                return i
        return None
    elif clic_valide_table(coordonee):
        return 10

def clic_valide_fabrique(coordonee, num_fabrique, NbJoueurs):
    ''' Verifie si le clic est dans une des fabriques '''
    n =(NbJoueurs * 2) + 1
    centrex =((longueur // n) // 4) +(num_fabrique *(longueur // n)) + tailleC
    centrey =(hauteur // 15)
    minx = centrex - tailleC
    miny = centrey - tailleC
    maxx = centrex + tailleC
    maxy = centrey + tailleC
    if coordonee[0]  > minx and coordonee[0] < maxx and coordonee[1] > miny and coordonee[1] < maxy:
        return True
    else:
        return False

def determiner_tuile_selectioner(coordonne, M, num_fabrique, NbJoueurs):
    ''' Détermine la couleur de la tuile où a cliqué le joueur'''
    n =(NbJoueurs * 2) + 1
    centrex =((longueur // n) // 4) +(num_fabrique *(longueur // n)) + tailleC
    centrey =(hauteur // 15)
    if coordonne[0] < centrex and coordonne[0] > centrex - tailleC :
        x = 0
    elif coordonne[0] > centrex and coordonne[0] < centrex + tailleC :
        x = 1
    else:
        x=None
    if coordonne[1] < centrey and coordonne[1] > centrey - tailleC:
        y = 0
    elif coordonne[1] > centrey and coordonne[1] < centrey + tailleC:
        y = 1
    else:
        y=None

    if x == None or y == None:
        return None

    if y == 0:
        return M[num_fabrique][x + y]
    else:
        return M[num_fabrique][x + y + 1]

def actualiser_fabrique(fabriques, num_fabrique):
    ''' Remplit la fabrique sélectionner de None, pour que les cases ne soient pas dessiner'''
    for i in range(len(fabriques[num_fabrique])):
        fabriques[num_fabrique][i] = None

def recup_clic():
    '''Récupère les coordonees du clic'''
    x, y, _ = attente_clic()
    return x, y

def compter_couleur_identique(lst, tuile):
    '''Compte le nombre de tuile de la même couleur que la tuile précédemment sélectionnée dans la fabrique'''
    nb = 0
    for i in range(len(lst)):
        if lst[i] == tuile:
            nb += 1
    return nb

def tuile_valide(tuile):
    '''Vérifie que la tuile sélectionnée ne vaut pas None'''
    if tuile == None:
        return False
    return True

def clic_valide_escalier(coordonee, numJoueur):
    ''' Vérifie que le clic du joueur se trouve dans son escalier'''
    if numJoueur % 2 == 0:
        minx = longueur//10
    else:
        minx = 6 * longueur//10
    if numJoueur < 2:
        miny =  3*hauteur//15
    else:
        miny =  10*hauteur//15

    maxx = minx + 7 * tailleC
    maxy = miny + 4/6*tailleC + 5*tailleC

    return not(coordonee[0]  < minx or coordonee[0] > maxx or coordonee[1] < miny or coordonee[1] > maxy)


def determiner_ligne_selectioner(coordonee, numJoueur):
    ''' Détermine quel ligne d'escalier ou plancher le joueur a sélectionné'''
    if numJoueur %2 == 0:
        XDebutPlancher = longueur//10
    else:
        XDebutPlancher = 6*longueur//10

    XFinPlancher = XDebutPlancher + 8*tailleC

    if numJoueur < 2:
        DebutPlancher =(3 * hauteur // 15) + 7/6*tailleC + 5*tailleC
        if int((coordonee[1] -(3 * hauteur // 15)) //(7/6 * tailleC)) < 5:
            return int((coordonee[1] -(3 * hauteur // 15)) //(7/6 * tailleC))
        elif coordonee[1]> DebutPlancher and coordonee[1]<DebutPlancher + tailleC and XDebutPlancher<coordonee[0] and coordonee[0]<XFinPlancher:
            return 5
    else:
        DebutPlancher =(10 * hauteur // 15) + 7/6*tailleC + 5*tailleC
        if int((coordonee[1] -(10 * hauteur // 15)) //(7/6 * tailleC)) < 5:
            return int((coordonee[1] -(10 * hauteur // 15)) //(7/6 * tailleC))
        elif coordonee[1]> DebutPlancher and coordonee[1] < DebutPlancher + tailleC and XDebutPlancher<coordonee[0] and coordonee[0]<XFinPlancher:
            return 5


def SelectionTuilesEtFabrique(fabriques, nbJoueurs, table):
    '''Renvoie la tuile sélectionée, la fabrique où a été sélectionnée la tuile et le nombre de tuile de cette couleur dans la fabrique'''
    fabrique = None
    while fabrique == None:
        coordonee=recup_clic()
        fabrique = determiner_fabrique_selectioner(coordonee, nbJoueurs)
    if fabrique == 10:
        tuile = determiner_tuile_selectioner_dans_table(coordonee, table)
        nb_tuile = table.count(tuile)
        SurbrillanceTable(table, tuile)
        return fabrique, tuile, nb_tuile, coordonee
    else:
        tuile = determiner_tuile_selectioner(coordonee, fabriques, fabrique, nbJoueurs)
        nb_tuile = compter_couleur_identique(fabriques[fabrique], tuile)
        SurbrillanceFabrique(fabriques, fabrique, tuile)
        return fabrique, tuile, nb_tuile, coordonee

def SelectionLigneEscalier(joueur):
    ''' Renvoie la ligne d'escalier ou le plancher selectionné par le joueur '''
    coordonee = recup_clic()
    ligne_escalier = determiner_ligne_selectioner(coordonee, joueur)
    if ligne_escalier == 5:
        return ligne_escalier
    else:
        while not clic_valide_escalier(coordonee, joueur):
            coordonee = recup_clic()
            ligne_escalier = determiner_ligne_selectioner(coordonee, joueur)
            if ligne_escalier == 5:
                break

    return ligne_escalier

def ConfirmerDeplacementDepuisFabrique(fabrique, tuile, nb_tuile, ligne_select, table, plancher, GenreJoueur):
    ''' Deplace les tuiles venant d'une fabrique vers le plateau d'un joueur si ce dernier a confirmer ce choix '''
    Dessine_boutons()
    if GenreJoueur == 'Bot':
        A_confirme = True
    else:
        A_confirme = confirmer()
    if A_confirme == False:
        update_ecran(NbJoueur, murs, planchers, escaliers, table, fabriques, score, num_joueur)
        return False
    else:
        PlaceDispo =(len(ligne_select) - ligne_select.count(None) - ligne_select.count(tuile) - 1)
        if PlaceDispo >= nb_tuile:
            TuileAPlaceDansEscalier =  nb_tuile
        else:
            TuileAPlaceDansEscalier = PlaceDispo

        FabriqueVersTable(table, fabriques[fabrique], tuile)
        actualiser_ligne_escalier(ligne_select, tuile, TuileAPlaceDansEscalier)
        actualiser_fabrique(fabriques, fabrique)

        if assez_de_place(nb_tuile, ligne_select,tuile) == False:
            tuile_a_placer_dans_plancher=nb_tuile-TuileAPlaceDansEscalier
            actualiser_plancher(plancher,tuile, tuile_a_placer_dans_plancher)
        update_ecran(NbJoueur, murs, planchers, escaliers, table, fabriques, score, num_joueur)
        return True

def DeroulementTour(NbJoueur, fabriques, joueur, escalier, table, plancher, GenreJoueur, murs, test):
    ''' Deplace les tuiles sélectionnés, vers la zone sélectionnés puis renvoie True, une fois finie'''
    if GenreJoueur == 'Humain':
        tuile = None
        while tuile == None:
            fabrique, tuile, nb_tuile, coordonee = SelectionTuilesEtFabrique(fabriques, NbJoueur, table)
            #FIXME Pas utile normalement
            # while not clic_valide_table(coordonee) and not clic_valide_fabrique(coordonee, fabrique, NbJoueur) :
            #     print('WHILE')
            #     coordonee = recup_clic()
            if clic_valide_fabrique(coordonee, fabrique, NbJoueur):
                if tuile == None:
                    continue
                ligne_escalier = SelectionLigneEscalier(joueur)
                if ligne_escalier == 5:
                    SurbrillancePlancher(joueur)
                    return ConfirmerDeplacementDepuisFabrique(fabrique, tuile, nb_tuile, plancher, table, plancher, GenreJoueur)
                else:
                    while not Ligne_Escalier_Valide(tuile, escalier[ligne_escalier]) or not CouleurDejaDansMur(tuile, murs[joueur][ligne_escalier]):
                        ligne_escalier = SelectionLigneEscalier(joueur)
                        if ligne_escalier == 5:
                            SurbrillancePlancher(joueur)
                            return ConfirmerDeplacementDepuisFabrique(fabrique, tuile, nb_tuile, plancher, table,plancher, GenreJoueur)
                    SurbrillanceEscalier(escalier, ligne_escalier, joueur)
                    return ConfirmerDeplacementDepuisFabrique(fabrique, tuile, nb_tuile, escalier[ligne_escalier], table,plancher, GenreJoueur)

            elif clic_valide_table(coordonee):
                tuile, nb_tuile = SelectionTuileTable(table, coordonee)
                if tuile == None:
                    break
                ligne_escalier = SelectionLigneEscalier(joueur)
                if ligne_escalier == 5:
                    SurbrillancePlancher(joueur)
                    return ConfirmerDeplacementDepuisTable(table, tuile, nb_tuile, plancher, plancher, GenreJoueur)
                else:
                    while not Ligne_Escalier_Valide(tuile, escalier[ligne_escalier]) or not CouleurDejaDansMur(tuile, murs[joueur][ligne_escalier]):
                        ligne_escalier = SelectionLigneEscalier(joueur)
                        if ligne_escalier == 5:
                            SurbrillancePlancher(joueur)
                            return ConfirmerDeplacementDepuisTable(table, tuile, nb_tuile, plancher, plancher, GenreJoueur)
                    SurbrillanceEscalier(escalier, ligne_escalier, joueur)
                    return ConfirmerDeplacementDepuisTable(table, tuile, nb_tuile, escalier[ligne_escalier],plancher, GenreJoueur)

    elif GenreJoueur == 'Bot':
        TourIA(fabriques,table,escaliers,planchers,num_joueur, GenreJoueur, murs, test)
        return True

def ConfirmerDeplacementDepuisTable(table, tuile, nb_tuile, ligne_select, plancher, GenreJoueur):
    ''' Deplace les tuiles venant du table vers le plateau d'un joueur si ce dernier a confirmer ce choix '''
    Dessine_boutons()
    if GenreJoueur == 'Bot':
        A_confirme = True
    else:
        A_confirme = confirmer()
    if A_confirme == False:
        update_ecran(NbJoueur, murs, planchers, escaliers, table, fabriques, score, num_joueur)
        return False
    else:
        if tuile == VJeton:
            tuile_a_placer_dans_plancher = 1
            actualiser_plancher(plancher,tuile, tuile_a_placer_dans_plancher)
        else:
            PlaceDispo =(len(ligne_select) - ligne_select.count(None) - ligne_select.count(tuile) - 1)
            if PlaceDispo >= nb_tuile:
                TuileAPlaceDansEscalier =  nb_tuile
            else:
                TuileAPlaceDansEscalier = PlaceDispo

            actualiser_ligne_escalier(ligne_select, tuile, TuileAPlaceDansEscalier)

            if assez_de_place(nb_tuile, ligne_select,tuile) == False:
                tuile_a_placer_dans_plancher=nb_tuile-TuileAPlaceDansEscalier
                actualiser_plancher(plancher,tuile, tuile_a_placer_dans_plancher)

            if table[0] == VJeton:      #Code Hexadécimal du jeton -1
                JetonPremierJoueurVersPlancher(table, plancher)               
            
        actualiser_table(table, tuile)
        update_ecran(NbJoueur, murs, planchers, escaliers, table, fabriques, score, num_joueur)
        return True

def actualiser_table(table, tuile):
    ''' Met à jour la matrice Table, en retirant les tuiles sélectionnées par le joueur pour les remplacer par des None, puis trie la matrice afin de mettre les None en fin de matrice '''
    for i in range(len(table)):
        if table[i] == tuile:
            table[i] = None
    NbDeNone = table.count(None)
    for i in range(NbDeNone):
        table.remove(None)
    table.sort()
    table.extend([None]*NbDeNone)

def JetonPremierJoueurVersPlancher(table, plancher):
    ''' Envoie le jeton vert premier joueur, vers le plancher du joueur qui a pioché dans le table en premier'''
    if table[0] == VJeton:
        table[0] = None

    for m in range(len(plancher)):
        if plancher[m] == '':
           plancher[m] = VJeton
           break

def clic_valide_table(coordonee):
    ''' Verifie si le joueur a cliqué dans le table '''
    minx = 4*longueur//10
    miny = 7*hauteur//15
    maxx = minx + 8*tailleC
    maxy = miny +4*tailleC + 3*tailleC//6
    if coordonee[0]  < minx or coordonee[0] > maxx or coordonee[1] < miny or coordonee[1] > maxy:
        return False
    else:
        return True

def SelectionTuileTable(table,coordonee):
    '''Renvoie la tuile sélectionée et le nombre de tuile de cette couleur dans le table'''
    tuile = determiner_tuile_selectioner_dans_table(coordonee, table)
    nb_tuile = table.count(tuile)
    SurbrillanceTable(table, tuile)
    return tuile, nb_tuile

def determiner_tuile_selectioner_dans_table(coordonne, table):
    ''' Détermine la couleur de la tuile où a cliqué le joueur, s'il a cliqué dans le table'''
    xInit = 4*longueur//10
    x = coordonne[0]
    for l in range(7):
        xTuile = xInit +(l+1)* 7*tailleC//6
        if x <= xTuile:
            j = l
            break

    yInit = 7*hauteur//15
    y = coordonne[1]
    for m in range(4):
        yTuile = yInit +(m+1)* 7*tailleC//6
        if y <= yTuile:
            i = m
            break
    return table[i*7+j]

def compter_couleur_identique_matrice(mat, tuile):
    '''Compte le nombre de tuile de la même couleur que la tuile du joueur '''
    nb = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == tuile:
                nb += 1
    return nb

def Ligne_Escalier_Valide(tuile, ligne_escalier):
    ''' Renvoie True, si la tuile peut être placé dans la ligne de l'escalier, et False si elle ne peut pas être placé'''
    if '' not in ligne_escalier:
        return False
    for i in range(len(ligne_escalier)):
        if ligne_escalier[i] not in [None, tuile, '', 'FlecheR', 'FlecheV']:
            return False
    return True

def FabriqueVersTable(table, Fabrique, tuile):
    ''' Deplace les tuiles restantes dans la fabrique sélectionnée vers le table'''
    j = 0
    for i in range(len(Fabrique)):
        if Fabrique[i] != tuile:
            while table[j] != None:
                j+=1
            table[j] = Fabrique[i]

def assez_de_place(nb_tuile, ligne_escalier, tuile):
    '''Renvoie True, si on peut placer toutes les tuiles sélectionnées dans la ligne d'escalier sélectionnée, et False sinon'''
    if nb_tuile >(len(ligne_escalier) - ligne_escalier.count(None) - ligne_escalier.count(tuile) - 1):
        return False
    return True

def actualiser_plancher(Lst_plancher,tuile, tuile_a_placer):
    ''' Met les tuiles qui doivent aller dans le plancher dans ce dernier'''
    for j in range(tuile_a_placer):
        for i in range(len(Lst_plancher)):
            if Lst_plancher[i] == '':
                Lst_plancher[i] = tuile
                break

def actualiser_ligne_escalier(ligne_escalier, tuile, nb_tuile):
    ''' Met autant de tuiles sélectionnés que possible dans la ligne escalier sélectionné'''
    longueur_ligne_escalier = len(ligne_escalier)
    for i in range(nb_tuile):
        for j in range(longueur_ligne_escalier):
            if ligne_escalier[j]  != None and ligne_escalier[j] != 'FlecheR' and ligne_escalier[j]  != 'FlecheV' and ligne_escalier[j] not in CouleurTuile and ligne_escalier[j] != VJeton :
                ligne_escalier[j] = tuile
                break


    if longueur_ligne_escalier == 6:
        if '' not in ligne_escalier:
            if ligne_escalier[-1] == 'FlecheV':
                ligne_escalier[-1] = 'FlecheR'
            else:
                ligne_escalier[-1] = 'FlecheV'

def alterner_joueur(num_joueur, nbjoueur):
    ''' Modifie le joueur jouant actuellement pour passer au joueur suivant'''
    new_num_joueur = num_joueur + 1
    if new_num_joueur > nbjoueur - 1:
        return 0
    return new_num_joueur

def Fabriques_vides(fabriques):
    ''' Renvoie True si toutes les fabriques sont vides'''
    n = len(fabriques)
    p = len(fabriques[0])
    for i in range(n):
        for j in range(p):
            if fabriques[i][j] != None:
                return False
    return True

def rotation_finie(fabriques, table):
    ''' Renvoie True, si la rotation actuelle est finie, c'est à dire s'il n'y pas plus de tuiles dans les fabrique et dans le table'''
    if not Fabriques_vides(fabriques) or table[0] != None:
        return False
    return True

def TourIA(fabriques,table,escaliers,planchers,num_joueur, GenreJoueur, murs, test):
    ''' Gère le tour d'un joueur IA de manière intelligente'''
    temps = 2.5
    if test == 1:
        temps = 0.5
    LstMarge=[0,-1,-2,1,2,-3,-4,3,4]
    for marge in LstMarge:
        TourFini = RemplirLignes(escaliers, murCoeff, murExemple, table, planchers, num_joueur, GenreJoueur, marge, temps)
        if TourFini:
            break
    if not TourFini:
        RecherchePourPlancher(table,planchers,fabriques,GenreJoueur)
    update_ecran(NbJoueur, murs, planchers, escaliers, table, fabriques, score, num_joueur)

def RemplirLignes(escaliers,murCoeff, murExemple, table,planchers,num_joueur, GenreJoueur, marge, temps):
    '''Remplit les lignes qui rapporte le plus de points'''
    for ligne in range(len(escaliers[num_joueur])-1,-1,-1):
        if escaliers[num_joueur][ligne][-2]=='':
            CouleurAPrendre, CasesARemplir = CasesAChercher(ligne,num_joueur,murExemple,murCoeff, escaliers)
            CasesARemplir = CasesARemplir + marge
            if CasesARemplir > 0:
                compteur,couleur,endroit,numFabrique = RechercheCase(CouleurAPrendre, CasesARemplir)
                if compteur!=None:
                    if endroit == "Table":
                        SurbrillanceTable(table,couleur)
                        SurbrillanceEscalier(escaliers[num_joueur], ligne, num_joueur)
                        mise_a_jour()
                        sleep(temps)
                        ConfirmerDeplacementDepuisTable(table, couleur, compteur, escaliers[num_joueur][ligne], planchers[num_joueur], GenreJoueur)
                        return True
                    elif endroit =="Fabriques":
                        SurbrillanceFabrique(fabriques, numFabrique, couleur)
                        SurbrillanceEscalier(escaliers[num_joueur], ligne, num_joueur)
                        mise_a_jour()
                        sleep(temps)
                        ConfirmerDeplacementDepuisFabrique(numFabrique, couleur, compteur, escaliers[num_joueur][ligne], table, planchers[num_joueur], GenreJoueur)
                        return True
    return False

def RecherchePourPlancher(table,planchers,fabriques,GenreJoueur):
    '''Cherche le nombre de cases minimum, si l'IA est obligé de jouer dans le plancher'''
    NbCase = 1
    while True:
        compteur,couleur,endroit,numFabrique = RechercheCase(['#FF4040','#4C5EFF','#80C324','#E1E1E1','#FFCC43'],NbCase)
        if compteur!=None:
            if endroit == "Table":
                SurbrillanceTable(table,couleur)
                SurbrillancePlancher(num_joueur)
                mise_a_jour()
                ConfirmerDeplacementDepuisTable(table, couleur, compteur, planchers[num_joueur], planchers[num_joueur], GenreJoueur)
                return 
            elif endroit =="Fabriques":
                SurbrillanceFabrique(fabriques, numFabrique, couleur)
                SurbrillancePlancher(num_joueur)
                mise_a_jour()
                ConfirmerDeplacementDepuisFabrique(numFabrique, couleur, compteur, planchers[num_joueur], table, planchers[num_joueur], GenreJoueur)
                return 
        NbCase+=1 

def CasesAChercher(numLigneEscalier,num_joueur,murExemple,murCoeff,escaliers):
    '''Définit le nombre de cases à chercher et leurs couleurs'''
    if escaliers[num_joueur][numLigneEscalier][-2-numLigneEscalier] != '':
        CouleurAPrendre = [escaliers[num_joueur][numLigneEscalier][-2-numLigneEscalier]]
    else:
        CouleurAPrendre=[]
        for case in range(len(murCoeff[num_joueur][numLigneEscalier])):
            if murCoeff[num_joueur][numLigneEscalier][case] == 0:
                CouleurAPrendre.append(murExemple[numLigneEscalier][case])
    CasesARemplir = escaliers[num_joueur][numLigneEscalier].count('')
    return CouleurAPrendre, CasesARemplir

def RechercheCase(LstCouleur, NbCases):
    '''L'IA cherche où elle peut trouver les cases dont elle a besoin'''
    # tailletable = len(table)
    # print("Recherche CASE TABLE",table)
    nbFabriques = len(fabriques)
    for couleur in LstCouleur:
        compteur = table.count(couleur)
        if compteur == NbCases:
            Endroit = "Table"
            return compteur,couleur,Endroit, None
        for numFabrique in range(nbFabriques):
            compteur = fabriques[numFabrique].count(couleur)
            if compteur == NbCases:
                Endroit = "Fabriques"
                return compteur,couleur,Endroit,numFabrique
    return None, None, None, None

def DeterminerPremierJoueur(planchers):
    for i in range(len(planchers)):
        if VJeton in planchers[i]:
            return i

def FinDeRotation(NbJoueur, escaliers, murs, murCoeff, murExemple, score, planchers):
    for numjoueur in range(NbJoueur):
        ExaminerLigne(numjoueur,escaliers,murs,murCoeff,murExemple)
        VideEscalier(numjoueur,escaliers)
        CalculMalus(numjoueur, planchers, score)
    return InitialiserPlanchers(NbJoueur)

def ExaminerLigne(num_joueur, escaliers, murs, murCoeff, murExemple):
    for ligne in range(len(escaliers[num_joueur])):
        if escaliers[num_joueur][ligne][-2] != '':
            Tuile = escaliers[num_joueur][ligne][-2]
            ActualisationMatFinDeTour(murExemple, murCoeff, murs, num_joueur, ligne, Tuile)

def ActualisationMatFinDeTour(murExemple, murCoeff, murs, num_joueur, ligne, Tuile):
    for i in range(len(murExemple[ligne])):
        if murExemple[ligne][i] == Tuile:
            murCoeff[num_joueur][ligne][i] = 1
            CalculPointsUneCase(num_joueur,score, (ligne,i),murCoeff)
            murs[num_joueur][ligne][i] = Tuile
            break

def case_valide(n,i,j):
    return (0 <= i <= (n - 1) and 0 <= j <= (n - 1))

def CalculPointsUneCase(num_joueur, score, coord, murCoeff):
    ComptV = 0
    n = len(murCoeff[num_joueur])
    for DepV in [-1,1]:
        i = coord[0] + DepV
        j = coord[1]
        while True:
            if case_valide(n,i,j) and murCoeff[num_joueur][i][j] == 1:
                ComptV += 1
                i += DepV
            else:
                break
    ComptH = 0
    for DepH in [-1,1]:
        i = coord[0]
        j = coord[1] + DepH
        while True:
            if case_valide(n,i,j) and murCoeff[num_joueur][i][j] == 1:
                ComptH += 1
                j += DepH
            else:
                break

    if ComptH>0 and ComptV >0:
        Compteur = ComptH+ComptV+2
    else:
        Compteur = ComptH+ComptV +1
    score[num_joueur]+=Compteur

def CalculMalus(num_joueur, planchers, score):
    for case in range(len(planchers[num_joueur])):
        if planchers[num_joueur][case] != '':
            if case <= 1:
                score[num_joueur] += -1
            elif case <=4:
                score[num_joueur] += -2
            else:
                score[num_joueur] += -3
        else:
            break

def VideEscalier(num_joueur, escaliers):
    n = len(escaliers[num_joueur][0])
    for ligne in range(len(escaliers[num_joueur])):
        if escaliers[num_joueur][ligne][-2] != '':
            Tuile = escaliers[num_joueur][ligne][-2]
            for i in range(n):
                if escaliers[num_joueur][ligne][i] == Tuile:
                    escaliers[num_joueur][ligne][i] =''
                escaliers[num_joueur][ligne][-1] = 'FlecheR'

def CouleurDejaDansMur(tuile, LigneDuMur):
    '''Verifie si la couleur de la tuile à placer est déjà dans le mur ou non'''
    if tuile in LigneDuMur:
        return False
    return True

def ChoixSauvegarde():
    x,y = recup_clic()
    while True:
        if  longueur//4 < x < 3*longueur//4 and 2*hauteur//6 < y < 3*hauteur//6:
            return True
        elif longueur//4 < x < 3*longueur//4 and 4*hauteur//6 < y < 5*hauteur//6:
            return False
        x,y = recup_clic()

def ConditionFinDePartie(murCoeff):
    '''renvoie un mur si ce dernier rempli la condition de fin de partie'''
    for mur in range(len(murCoeff)):
        for ligne in murCoeff[mur]:
            if ligne == [1,1,1,1,1]:
                return mur

################## Calcul des bonus ############################################
def BonusScore(nbjoueur, score, murCoeff, murs):
    for i in range(nbjoueur):
        score[i] = BonusLigne(murCoeff[i],score[i])
        score[i] = BonusColonne(murCoeff[i],score[i])
        score[i] = BonusCouleur(murs[i], score[i])
    return score

def BonusLigne(matcoeff, score):
    for ligne in matcoeff:
        if ligne == [1,1,1,1,1]:
            score += 2
    return score

def BonusColonne(matcoeff, score):
    n=len(matcoeff)
    for i in range(len(matcoeff[0])):
        Colonne = True
        for j in range(n):
            if matcoeff[j][i] == 0:
                Colonne = False
                break
        if Colonne:
            score += 7
    return score

def BonusCouleur(mur, score):
    Dico = {R :0, Bl :0, Bc:0, V:0, J:0}
    for ligne in mur:
        for case in ligne:
            if case == R:
                Dico[R]+=1
            elif case == Bl:
                Dico[Bl]+=1
            elif case == Bc:
                Dico[Bc]+=1
            elif case == V:
                Dico[V]+=1
            elif case == J:
                Dico[J]+=1
    for valeur in Dico.values():
        if valeur >= 5:
            score += 10
    return score

################################################################################

if __name__ == '__main__':

    num_joueur = 0

    cree_fenetre(longueur, hauteur)

########## Initialisation des matrices et affichage de l'ecran #################
    Save = 'Save.txt'
    DebutPartie()
    Choix = ChoixSauvegarde()
    if Choix:
        Fichier = input("Choisir le fichier contenant votre matrice ")
        murExemple, murJoueur = LectureMatDepart(Fichier)
        NbJoueur, ListeTypeJoueur, test = EcranChoixNbJoueur()
        sac = InitialiserSac()
        fabriques = RemplirFabrique(NbJoueur, sac)
        murs = InitialiserMurs(NbJoueur, murJoueur)
        planchers = InitialiserPlanchers(NbJoueur)
        escaliers = InitialiserEscaliers(NbJoueur)
        table = InitialiserTable()
        score = InitialiserScore(NbJoueur)
        murCoeff = InitialiserCoeffMur(NbJoueur)
    else:
        NbJoueur,ListeTypeJoueur,sac,fabriques,murs,planchers,escaliers,table,score,murCoeff,murExemple,num_joueur,test = LectureFichierSauvegarde(Save)

################################################################################

######################### Boucle principale du jeu #############################
    update_ecran(NbJoueur,murs,planchers,escaliers,table,fabriques,score, num_joueur)
    #quadrillage()
    while True:
        EcritureFichierSauvegarde(Save, NbJoueur,ListeTypeJoueur,sac,fabriques,murs,planchers,escaliers,table,score,murCoeff,murExemple,num_joueur, test)
        tour_fini = DeroulementTour(NbJoueur, fabriques, num_joueur, escaliers[num_joueur], table, planchers[num_joueur], ListeTypeJoueur[num_joueur], murs, test)
        while not tour_fini:
            tour_fini = DeroulementTour(NbJoueur, fabriques, num_joueur, escaliers[num_joueur], table, planchers[num_joueur], ListeTypeJoueur[num_joueur], murs, test)
        num_joueur = alterner_joueur(num_joueur, NbJoueur)
        if rotation_finie(fabriques, table):
            if len(sac)==0:
                sac=InitialiserSac()
            fabriques = RemplirFabrique(NbJoueur, sac)
            num_joueur = DeterminerPremierJoueur(planchers)
            table[0] = VJeton
            planchers = FinDeRotation(NbJoueur, escaliers, murs, murCoeff, murExemple, score, planchers)
        update_ecran(NbJoueur,murs,planchers,escaliers,table,fabriques,score, num_joueur)
        condition = ConditionFinDePartie(murCoeff)
        if condition != None:
            score = BonusScore(NbJoueur, score, murCoeff, murs)
            update_ecran(NbJoueur,murs,planchers,escaliers,table,fabriques,score, num_joueur)
            break

################################################################################
    # Afficher gagnant et score de chacun
    sleep(2)
    Dessine_ecran_fin(score, NbJoueur, condition)
    print('Cliquez n\'importe où sur l\'écran')
    attente_clic()
    ferme_fenetre()
