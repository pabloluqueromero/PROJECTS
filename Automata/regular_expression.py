import re
from functools import partial,lru_cache
from collections import defaultdict
from graph import Graph,Node,Edge

class RegularExpresion:
    def __init__(self,elements,expresion):
        self.elem = elements
        self.expr = expresion #Must be without brackets
        
    def parse_parenthesis(self,expr):
        counter = 0
        l=[]
        left=0
        for i in range(len(expr)):
            if expr[i] == '(':
                counter+=1
            elif expr[i] == ')':
                counter-=1
                if counter == 0:
                    l.append(expr[left:i+1])
                    left=i+1
            elif counter == 0:
                l.append(expr[i])
                left+=1
        return l
    
    def empty_word(self,s):
        if len(s)>1 and s[1]=='*':
            return True
        
        return ('+Ɛ+' in s[0] or '+Ɛ' in s[0] or 'Ɛ+' in s[0])

    @lru_cache(None)
    def differentiate(self,d,expr):
        # contains_parentheis = lambda s: len(s)>0 and re.match("") 
        epsilon='Ɛ'
        void ='∅' 
        # RULE 1: Same symbol as derivation symbol
        if expr == '(' or expr ==')' or expr == '':
            return expr
        if expr == d:
            return epsilon
        # RULE 2: Different symbol as derivation symbol    
        if  len(expr)==1 and expr!=d:
            return void
        
        # RULE 3: Separate additions
        s = self.parse_parenthesis(expr)
        derivatives = []
        left = 0

        #if no additions differentiate first elements which must have parenthesis
        #if no additions differentiate first elements which must have parenthesis
        if len(s)==1:
            return '('+ self.differentiate(d,''.join(s[0][1:-1]))+')'

        for i in range(len(s)):
            if s[i] == '+':
                alpha = ''.join(s[left:i])
                derivatives.append(self.differentiate(d,alpha))
                left = i+1
        #If there are additions operate with them and add the last bit
        if derivatives:
            alpha = ''.join(s[left:])
            derivatives.append(self.differentiate(d,alpha))
            return '+'.join(derivatives)

        #RULE 5: One structure with Kleene star
        if len(s)==2 and s[1]=='*':
            alpha = ''.join(s[0])
            return self.differentiate(d,alpha) + expr

        #RULE 4: Multiplications - if contains epsilon we add derivate of Beta
        if self.empty_word(s):
            if s[1] == '*': 
                alpha = ''.join(s[:2])
                beta = ''.join(s[2:])
            else:
                alpha = ''.join(s[:1])
                beta = ''.join(s[1:])
            return self.differentiate(d,alpha)+beta+'+'+self.differentiate(d,beta)
        else:
            alpha = ''.join(s[:1])
            beta = ''.join(s[1:])
            return self.differentiate(d,alpha) + beta

    def replace(self,alpha):
        alpha=alpha.replace('+∅+','')
        alpha=alpha.replace('+∅','')
        alpha=alpha.replace('∅+','')
        alpha=alpha.replace('()','')
        alpha=alpha.replace('(Ɛ)','Ɛ')
        alpha=alpha.replace('Ɛ(','(')
        for e in self.elem: 
            alpha=alpha.replace('Ɛ'+e,e)
        alpha=alpha.replace('(∅)','∅')
        return alpha
    
    def clean_expression(self,expr):
        epsilon='Ɛ'
        void ='∅'
        s = self.parse_parenthesis(expr)
        plus_sign = []
        left=0
        for i in range(len(s)):
            if s[i] == '+':
                if '∅' not in s[left:i]:
                    alpha = ''.join(s[left:i])
                    alpha=self.replace(alpha)
                    plus_sign.append(alpha)
                left = i+1

        if left!=0:
            if '∅' not in s[left:]:
                alpha = ''.join(s[left:])
                alpha=self.replace(alpha)
                plus_sign.append(alpha)
                return '+'.join(plus_sign)
            elif plus_sign:
                return '+'.join(plus_sign)
            return '∅'
        if '∅' in s:
            return '∅'
        else:
            expr=self.replace(expr)
            return expr

    def full_derivative(self):
        open_expressions=set()
        solved=set()
        open_expressions.add(('',self.expr))
        solved.add(self.expr)
        solution=dict()
        solution['']=(self.expr,self.expr) #(before,after)   First one->Ɛ
        while open_expressions:
            p,ex = open_expressions.pop()
            for e in self.elem:
                s = self.differentiate(e,ex) 
                cleaned = self.clean_expression(s)
                old = s
                while cleaned != old:
                    old=cleaned
                    cleaned = self.clean_expression(old)
                    #print('{:25s} -- {} ------> {}'.format(ex,e+p,cleaned))
                    #print('D {:7s} [{}] ={}'.format(p+e,ex,cleaned))
                if cleaned not in solved :
                    solved.add(cleaned)
                    if cleaned!='∅' and cleaned != 'Ɛ':
                        open_expressions.add((p+e,cleaned))
                solution[p+e]=(ex,cleaned)
        return solution

    def build_automata(self,d):
        processed=dict()
        g = Graph()
        for key,value in sorted(d.items(),key = lambda x: len(x[0])):
            value=value[1]
            if value=='∅':
                continue
            if value in processed:
                previous = key[:-1]
                if d[key[:-1]][1] in processed:
                    previous= processed[d[key[:-1]][1]]
                g.add_edge(Edge(previous,processed[value],key[-1]))
            else:
                g.add_node(Node(key))
                if len(key)>0:
                    g.add_edge(Edge(key[:-1],key,key[-1]))
                processed[value]=key
        return g



#DRIVER CODE
expr = '0(1+0)*0+11(1+0)(1+0)*0'
elem = {'0','1'}
regex = RegularExpresion(elem,expr)

#DERIVATIVE
print("DERIVATIVES:")
sol=regex.full_derivative()
for key,val in sorted(sol.items(),key = lambda x: len(x[0])): 
    print('D {:7s} [{}] ={}'.format(key,val[0],val[1]))


print("\nAUTOMATA:")
g = regex.build_automata(sol)
print('States: ', [node.tag for node in g.get_nodes()])
print('Transitions: ')
for a in g.get_edges():
    print('  ',a.tag ,': ', a.node1,' -> ',a.node2)