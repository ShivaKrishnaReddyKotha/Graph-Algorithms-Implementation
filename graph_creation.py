#Dictionary Creation
import pandas as pd
from unidecode import unidecode


class TitleDictionary:

    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df["primaryTitle"] = self.df["primaryTitle"].apply(unidecode)
        self.title_dict = self._create_title_dict()
        self.profession_dict = self._create_profession_dict()

    def _create_title_dict(self):
        
        title_dict = {}
        
        for i, rowData in self.df.iterrows():
            nconst = rowData['nconst']
            if nconst not in title_dict:
                title_dict[nconst] = []
            title_dict[nconst].append(rowData['primaryTitle'])

        return title_dict
        
    
    def _create_profession_dict(self):
        
        profession_dict = {}

        for i, rowData in self.df.iterrows():
            nconst = rowData['nconst']
            if nconst not in profession_dict:
                profession_dict[nconst] = []
            profession_dict[nconst].append(rowData['primaryProfession'])
        profession_dict

        return profession_dict


#Graph Network Creation
class MovieNetwork:
    def __init__(self, name_movie_dict, nconst_ar_dr):
        self.graph = {} 
        self.name_movie_dict = name_movie_dict 
        self.nconst_ar_dr = nconst_ar_dr 

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}
            
    def add_edge(self, node1, node2, nconst_ar_dr, weight=1):
        if node1 == node2:
            return

        if weight <= 2:
            return

        ProfessionOfNode1 = self.nconst_ar_dr.get(node1, '')
        if isinstance(ProfessionOfNode1, list):
            ProfessionOfNode1 = '_'.join(ProfessionOfNode1)
        ProfessionOfNode1 = ProfessionOfNode1.split('_')[-1]
    
        ProfessionOfNode2 = self.nconst_ar_dr.get(node2, '')
        if isinstance(ProfessionOfNode2, list):
            ProfessionOfNode2 = '_'.join(ProfessionOfNode2)
        ProfessionOfNode2 = ProfessionOfNode2.split('_')[-1]

        
        if ProfessionOfNode1 == 'actor' and ProfessionOfNode2 == 'director':
            if node2 not in self.graph:
                self.graph[node2] = {}
            self.graph[node2][node1] = weight
        elif ProfessionOfNode1 == 'director' and ProfessionOfNode2 == 'actor':
            if node1 not in self.graph:
                self.graph[node1] = {}
            self.graph[node1][node2] = weight
        elif ProfessionOfNode1 == 'actor' and ProfessionOfNode2 == 'actor':
            if node1 not in self.graph:
                self.graph[node1] = {}
            if node2 not in self.graph:
                self.graph[node2] = {}
            self.graph[node1][node2] = weight
            self.graph[node2][node1] = weight
        elif ProfessionOfNode1 == 'director' and ProfessionOfNode2 == 'director':
            if node1 not in self.graph:
                self.graph[node1] = {}
            if node2 not in self.graph:
                self.graph[node2] = {}
            self.graph[node1][node2] = weight
            self.graph[node2][node1] = weight
        else:
            if node1 not in self.graph:
                self.graph[node1] = {}
            if node2 not in self.graph:
                self.graph[node2] = {}
            self.graph[node1][node2] = weight
            self.graph[node2][node1] = weight


        
                
    def create_graph(self):

        for node1 in self.name_movie_dict:
            self.add_node(node1)
            for node2 in self.name_movie_dict:
                if node1 != node2:
                    weight=len(set(self.name_movie_dict[node1]).intersection(set(self.name_movie_dict[node2])))
                    self.add_edge(node1, node2, self.nconst_ar_dr, weight)

        return self.graph
        
