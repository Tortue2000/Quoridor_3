import networkx as nx


class QuoridorError(Exception):
    def __str__(self):
        if self.args and self.args[0]:
            return f'QuoridorError: «{self.args[0]}»'
        return 'QuoridorError'


def soulever_mon_erreur(mess):
    raise QuoridorError(mess)

class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Attributes:
        état (dict): état du jeu tenu à jour.
        Identifiez les autres attribut de votre classe

    Examples:
        >>> q.Quoridor()
    """
    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe Quoridor.

        Initialise une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        Args:
            joueurs (List): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
                Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
                l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut
                initialement placer 10 murs. Dans le cas où l'argument est un dictionnaire,
                celui-ci doit contenir une clé 'nom' identifiant le joueur, une clé 'murs'
                spécifiant le nombre de murs qu'il peut encore placer, et une clé 'pos' qui
                spécifie sa position (x, y) actuelle. Notez que les positions peuvent être sous
                forme de tuple (x, y) ou de liste [x, y].
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions (x, y) des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions (x, y) des murs verticaux. Par défaut, il
                n'y a aucun mur placé sur le jeu. Notez que les positions peuvent être sous
                forme de tuple (x, y) ou de liste [x, y].

        Raises:
            QuoridorError: L'argument 'joueurs' n'est pas itérable.
            QuoridorError: L'itérable de joueurs en contient un nombre différent de deux.
            QuoridorError: Le nombre de murs qu'un joueur peut placer est plus grand que 10,
                            ou négatif.
            QuoridorError: La position d'un joueur est invalide.
            QuoridorError: L'argument 'murs' n'est pas un dictionnaire lorsque présent.
            QuoridorError: Le total des murs placés et plaçables n'est pas égal à 20.
            QuoridorError: La position d'un mur est invalide.
        """
        self.joueurs = joueurs
        self.murs = murs

        ty = type(self.joueurs)
        if  ty == str or ty == tuple or ty == list or ty == dict or ty == set:
	            pass
        else:
            soulever_mon_erreur("L'argument 'joueurs' n'est pas itérable.")

        if len(self.joueurs) == 2:
	            pass
        else:
	            soulever_mon_erreur(
                    "L'itérable de joueurs en contient un nombre différent de deux."
                    )

        if type(self.joueurs[0]) == dict:
            if self.joueurs[0]['murs'] > 10 or self.joueurs[0]['murs'] < 0:
                soulever_mon_erreur(
                    "Le nombre de murs qu'un joueur peut placer est plus grand que 10, ou négatif."
                    )
        if type(self.joueurs[1]) == dict:
            if self.joueurs[1]['murs'] > 10 or self.joueurs[1]['murs'] < 0:
                soulever_mon_erreur(
                    "Le nombre de murs qu'un joueur peut placer est plus grand que 10, ou négatif."
                    )

        if type(self.joueurs[0]) == dict:
            if not (0 < self.joueurs[0]['pos'][0] < 10) or not(0 < self.joueurs[0]['pos'][1] < 10):
                soulever_mon_erreur("La position d'un joueur est invalide.")
        if type(self.joueurs[1]) == dict:
            if not(0 < self.joueurs[1]['pos'][0] < 10) or not( 0 < self.joueurs[1]['pos'][1] < 10):
                soulever_mon_erreur("La position d'un joueur est invalide.")

        if not (type(self.murs) == dict) and not (self.murs == None):
            soulever_mon_erreur(
                "L'argument 'murs' n'est pas un dictionnaire lorsque présent."
                )

        if type(self.joueurs[0]) == dict:
            h = self.murs['horizontaux']
            v = self.murs['verticaux']
            n1 = self.joueurs[0]['murs']
            n2 = self.joueurs[1]['murs']
            if not (len(h) + len(v) + n1 + n2 == 20):
                soulever_mon_erreur("Le total des murs placés et plaçables n'est pas égal à 20.")

        if type(self.murs) == dict:
            for cle in self.murs['horizontaux']:
                if not(0 < cle[0] < 9) or not( 1 < cle[1] < 10):
                    soulever_mon_erreur("La position d'un mur est invalide.")

            for cle in self.murs['verticaux']:
                if not(1 < cle[0] < 10) or not( 0 < cle[1] < 9):
                    soulever_mon_erreur("La position d'un mur est invalide.")

        self.etat_partie = {'joueurs': self.joueurs, "murs": self.murs}
        if type(self.joueurs[0]) == str and type(self.joueurs[1]) == str:
            self.etat_partie = {'joueurs':[{"nom": joueurs[0], "murs": 10, "pos": (5, 1)}, {"nom": joueurs[1], "murs": 10, "pos": (5, 9)}], "murs": self.murs}



    def __str__(self):

        grille_de_base = [['   ' + '-'*35],
        ['9 |', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ',
         ' . ', ' ', ' . ', '|'],
        ['  |', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ',
         '   ', ' ', '   ', '|'],
        ['8 |', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ',
         ' . ', ' ', ' . ', '|'],
        ['  |', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ',
         '   ', ' ', '   ', '|'],
        ['7 |', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ',
         ' . ', ' ', ' . ', '|'],
        ['  |', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ',
         '   ', ' ', '   ', '|'],
        ['6 |', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ',
         ' . ', ' ', ' . ', '|'],
        ['  |', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ',
         '   ', ' ', '   ', '|'],
        ['5 |', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ',
         ' . ', ' ', ' . ', '|'],
        ['  |', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ',
         '   ', ' ', '   ', '|'],
        ['4 |', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ',
         ' . ', ' ', ' . ', '|'],
        ['  |', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ',
         '   ', ' ', '   ', '|'],
        ['3 |', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ',
         ' . ', ' ', ' . ', '|'],
        ['  |', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ',
         '   ', ' ', '   ', '|'],
        ['2 |', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ',
         ' . ', ' ', ' . ', '|'],
        ['  |', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ', '   ', ' ',
         '   ', ' ', '   ', '|'],
        ['1 |', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ', ' . ', ' ',
         ' . ', ' ', ' . ', '|'],
        ['--|' + '-'*35],
        ['  | 1   2   3   4   5   6   7   8   9']]

        for i in self.etat_partie["murs"]["horizontaux"]:
            grille_de_base[17 - (i[1]*2) + 3][((i[0] - 1) *2 )+ 1] = '---'
            grille_de_base[17 - (i[1]*2) + 3][((i[0] - 1) *2 )+ 2] = '-'
            grille_de_base[17 - (i[1]*2) + 3][((i[0] - 1) *2 )+ 3] = '---'

        for i in self.etat_partie["murs"]["verticaux"]:
            grille_de_base[17 - ((i[1] - 1)*2)][((i[0] - 1) *2 )] = '|'
            grille_de_base[17 - ((i[1] - 1)*2) - 1][(i[0] - 1) *2] = '|'
            grille_de_base[17 - ((i[1] - 1)*2) - 2][(i[0] - 1) *2] = '|'


        a0 = self.etat_partie.get("joueurs")[0]
        b0 = a0["pos"]
        grille_de_base[17 - ((b0[1] - 1)*2)][((b0[0]-1)*2) +1] = ' 1 '


        a1 = self.etat_partie.get("joueurs")[1] 
        b1 =  a1["pos"] 
        grille_de_base[17 - ((b1[1] - 1)*2)][((b1[0]-1)*2) +1] = ' 2 '

        n1 = self.etat_partie["joueurs"][0]["nom"]
        n2 = self.etat_partie["joueurs"][1]["nom"]
        nb1 = self.etat_partie["joueurs"][0]["murs"]
        nb2 = self.etat_partie["joueurs"][1]["murs"]
        if len(n1) > len(n2):
            espace2 = len(n1)-len(n2)
            espace1 = 0
        elif len(n1) < len(n2):
            espace1 = len(n2)-len(n1)
            espace2 = 0
        else:
            espace1 = 0
            espace2 = 0

        print('Légende:')
        print('   1=', n1, ', ', ' ' * espace1 , end='', sep = '')
        print('murs=', '|'*nb1)
        print('   2=', n2, ', ', ' ' * espace2 , end='', sep = '')
        print('murs=', '|'*nb2)

        for i in range(20):
            print(*grille_de_base[i], sep= '')

    def déplacer_jeton(self, joueur, position):
        """Déplace un jeton.

        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
            position (Tuple[int, int]): Le tuple (x, y) de la position du jeton 
            (1<=x<=9 et 1<=y<=9).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """
        if joueur != 1 and joueur != 2:
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')
        if 1 <= position[0] <= 9 == False or 1 <= position[1] <= 9 == False:
            raise QuoridorError('La position est invalide (en dehors du damier).')

        graphique = construire_graphe(
        [joueur['pos'] for joueur in self.etat_partie['joueurs']],
        self.etat_partie['murs']['horizontaux'],
        self.etat_partie['murs']['verticaux'])

        if joueur == 1:
            position_actuelle = self.etat_partie['joueurs'][0]['pos']
        if joueur == 2:
            position_actuelle = self.etat_partie['joueurs'][0]['pos']
        position_possible = list(graphique.successors(position_actuelle))
        if position in position_possible == False:
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")

        else:
            if joueur == 1:
                self.etat_partie['joueurs'][0]['pos'] = position
            if joueur == 2:
                self.etat_partie['joueurs'][1]['pos'] = position
        return self.etat_partie

    def état_partie(self):
        """Produire l'état actuel de la partie.

        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                  Notez que les positions doivent être sous forme de tuple (x, y) uniquement.

        Examples:

            {
                'joueurs': [
                    {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                    {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
                ],
                'murs': {
                    'horizontaux': [...],
                    'verticaux': [...],
                }
            }

            où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
            au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
            associée à sa position sur le damier. Une position est représentée par un tuple
            de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

            Les murs actuellement placés sur le damier sont énumérés dans deux listes de
            positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
            est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
            situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
            mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """
        return self.etat_partie

    def jouer_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La partie est déjà terminée.

        Returns:
            Tuple[str, Tuple[int, int]]: Un tuple composé du type et de la position du coup joué.
        """
        import random

        graphe = construire_graphe(
        [joueur['pos'] for joueur in self.etat_partie['joueurs']],
        self.etat_partie['murs']['horizontaux'],
        self.etat_partie['murs']['verticaux'])

        if joueur == 1:
            if len(nx.shortest_path(graphe, self.etat_partie['joueurs'][0]['pos'], 'B1')) > len(nx.shortest_path(graphe, self.etat_partie['joueurs'][1]['pos'], 'B2')):
                type_du_coup = 'PLACER UN MUR'
                x1 = random.randint(0, 9)
                y1 = random.randint(0, 9)
                pos1 = (x1, y1)
                orientation = random.choice( ['horizontal', 'vertical'] )
                self.placer_mur(1, pos1, orientation)
            else:
                type_du_coup = 'déplacer un jeton'
                pos1 = nx.shortest_path(graphe, self.etat_partie['joueurs'][0]['pos'], 'B1')[1]
                self.déplacer_jeton(1, pos1)
        elif joueur == 2:
            if len(nx.shortest_path(graphe, self.etat_partie['joueurs'][0]['pos'], 'B1')) < len(nx.shortest_path(graphe, self.etat_partie['joueurs'][1]['pos'], 'B2')):
                type_du_coup = 'PLACER UN MUR'
                x1 = random.randint(0, 9)
                y1 = random.randint(0, 9)
                pos1 = (x1, y1)
                orientation = random.choice( ['horizontal', 'vertical'] )
                self.placer_mur(2, pos1, orientation)
            else:
                type_du_coup = 'déplacer un jeton'
                pos1 = nx.shortest_path(graphe, self.etat_partie['joueurs'][1]['pos'], 'B2')[1]
                self.déplacer_jeton(2, pos1)

            return (type_du_coup, pos1)


    def partie_terminée(self):
        """Déterminer si la partie est terminée.

        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        if self.joueurs[0]['pos'][1] == 9:
            return self.joueurs[0]['nom']
        if self.joueurs[1]['pos'][1] == 1:
            return self.joueurs[0]['nom']
        else:
            return False

    def placer_mur(self, joueur, position, orientation):
        """Placer un mur.

        Pour le joueur spécifié, placer un mur à la position spécifiée.

        Args:
            joueur (int): le numéro du joueur (1 ou 2).
            position (Tuple[int, int]): le tuple (x, y) de la position du mur.
            orientation (str): l'orientation du mur ('horizontal' ou 'vertical').

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: La position est invalide pour cette orientation.
            QuoridorError: Le joueur a déjà placé tous ses murs.
        """
        if orientation == 'vertical':
            orientation_mur = "verticaux"
        if orientation == "horizontal":
            orientation_mur = "horizontaux"

        if joueur != 1 and joueur != 2:
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')

        if position in (self.etat_partie['murs'][orientation_mur]) == True:
            raise QuoridorError('un mur occupe déjà cette position.')

        if orientation == 'horizontal' and (position[0] <= 1 or position[0] >= 9):
            raise QuoridorError('La position est invalide pour cette orientation.')

        if orientation == 'vertical' and (position[1] <= 1 or position[1] >= 9):
            raise QuoridorError('La position est invalide pour cette orientation.')

        if joueur == 1 and self.etat_partie['joueurs'][0]['murs'] == 0:
            raise QuoridorError('Le joueur a déjà placé tous ses murs.')

        if joueur == 2 and self.etat_partie['joueurs'][1]['murs'] == 0:
            raise QuoridorError('Le joueur a déjà placé tous ses murs')

        self.etat_partie['murs'][orientation_mur].append(position)
        self.etat_partie["joueurs"][joueur - 1]["murs"] -= 1

        graphique = construire_graphe(
        [joueur['pos'] for joueur in self.etat_partie['joueurs']], 
        self.etat_partie['murs']['horizontaux'],
        self.etat_partie['murs']['verticaux'])

        if nx.has_path(graphique, self.etat_partie["joueurs"][0]["pos"], 'B1') == False or nx.has_path(graphique, self.etat_partie["joueurs"][1]["pos"], 'B2') == False:
            self.etat_partie['murs'][orientation_mur].remove(position)
            self.etat_partie["joueurs"][joueur - 1]["murs"] += 1
            raise QuoridorError("La position est invalide pour cette orientation.")
        return self.etat_partie


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """Construire un graphe de la grille.

    Crée le graphe des déplacements admissibles pour les joueurs.
    Vous n'avez pas à modifer cette fonction.

    Args:
        joueurs (List[Tuple]): une liste des positions (x,y) des joueurs.
        murs_horizontaux (List[Tuple]): une liste des positions (x,y) des murs horizontaux.
        murs_verticaux (List[Tuple]): une liste des positions (x,y) des murs verticaux.

    Returns:
        DiGraph: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe

from quoridor import Quoridor
quoridor_test_1 = Quoridor(joueurs=['joueur1', 'joueur2'], murs = {"horizontaux": [(2, 2), (4, 4)], "verticaux": [(4, 7), (3, 2)]})
quoridor_test_1.__str__()
quoridor_test_1.déplacer_jeton(1, (5, 2))
quoridor_test_1.__str__()