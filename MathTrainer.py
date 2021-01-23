# -*- coding: utf-8 -*-
"""
Created on Sun May 31 08:44:33 2020

WxPython
    https://stackoverflow.com/questions/18532827/using-wxpython-to-get-input-from-user
    https://en.wikipedia.org/wiki/Learning_curve


@author: 危機
"""

"""
MATH:
    Addition & Substraction:
        Modulus Addition & Substraction
        Residual Addition & Substraction
        Fractions
    Multiplication & Division:
    
    Powers:
        Raise Fractions to Powers
        Powers to Powers
        Fractions Sumplification of Powers

    Algebra:
        Addition & Substraction of Polynomials:
            Random number of summations
            Fractional Coefficients
            Fractional Degrees

        Multiplication & Division of Polynomials:
            Fractional Coefficients
            1st Degree
            Mix from 0th to nth degree
            Fractional Degrees

        Factorization
            Fractional Coefficients
            1st Degree
            Mix from 0th to nth degree
            Fractional Degrees

        Functions
            Find numerical value
        
        Polynomials Raised to Powers:
            Powers
        
        Chapter XI Baldor Algebra
        Maximum Common Divisor
            M.C.D. of 2 to n Polynomials
        Minimum Common Divisor
            M.C.D. of 2 to n Polynomials 
        Equations
            Physics
            
        Inequalities

Procedure:
    Start with an easy level and go increasing the difficulty untill a breakpoint
    then start with the second last successful level
    
    https://docs.sympy.org/latest/modules/parsing.html
    https://stackoverflow.com/questions/48531276/how-to-create-symbol-polynomial-from-given-array-with-sympy

    https://guao.org/sites/default/files/biblioteca/%C3%81lgebra%20de%20Baldor.pdf


    https://docs.sympy.org/latest/modules/polys/reference.html
    https://docs.sympy.org/latest/tutorial/simplification.html
    https://docs.sympy.org/latest/modules/polys/index.html

"""


"""
Total problems:
    10 Levels
        Part A 10*5
        Part B 10*5
    
    Thresh:
        90% Right
        75% Above Time
        
"""

"""
Thresholds

After passing a level put a higher thresh

Thread the timer
Adapt the timer

Adapt levels
    Level down when many failed
    2 Levels up if perfect or near perfect
    2 Levels down if very bad
    
    Find specific tasks:
        Specific Multiplications table
        Specific Functions

"""


"""
Training session:
    Select topics and the number of levels or number of tries for every topic
        Learning Curves and Forgetting Curves
    Intensity of the training:
        
    
    
"""


"""
Matrices:
    Addition-Substraction
    Multiplication
    Gauss Jordan
    Finding Rotation, Identity, Exchange matrices
    
Factorization
    Fractional Coefficients
    1st Degree
    Mix from 0th to nth degree
    Fractional Degrees

Calculus
    Derivatives:
        Based on the derivative formulas in cheatsheets solve problems. These are the blueprints
    Integrals:
        Based on the integral formulas in cheatsheets solve problems. These are the blueprints
    
    Multivariate Cilindrical and Spherical Coordinates:
        
    


"""

# =============================================================================
# %% Settings
# =============================================================================

'''
Add Sign to the mat variable that is saved in the settings
Check if everything needed to reconstruct the problem is saved in the settings dict

https://docs.sympy.org/latest/modules/evalf.html
https://docs.sympy.org/latest/modules/evalf.html
https://docs.sympy.org/latest/tutorial/manipulation.html



https://tex.stackexchange.com/questions/503342/display-content-in-two-column-layout-in-pylatex
https://stackoverflow.com/questions/36560642/pylatex-basic-script-wont-run-because-script-interpreter-could-not-be-found
'''



# =============================================================================
# %% PATH
# =============================================================================
PATH = 'D:/LifeWare Technologies/Math Trainer/Hist/'
exercises_PATH = 'D:/LifeWare Technologies/Math Trainer/Exercises/'



# =============================================================================
# %% Libs
# =============================================================================
import sympy as spy, os, numpy as np, winsound
#from sympy import init_printing
from time import time, sleep
import datetime

from sympy import symbols, simplify, Function, Symbol, init_session, latex
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
from sympy.printing.mathml import print_mathml
#init_session()
#spy.init_printing()

from pylatex import Document, Section, Subsection, Command, Math
from pylatex.utils import italic, NoEscape
from pylatex.package import Package
from pylatex import PageStyle, Head, MiniPage, Foot, LargeText, MediumText, LineBreak, simple_page_number
from pylatex.utils import bold


# =============================================================================
    # %% Sympy Settings
# =============================================================================

transformations = (standard_transformations + (implicit_multiplication_application,))

# =============================================================================
# %% Defs
# =============================================================================

def intNumLevel(level,n,n_probs): # Returns the set of problems for this level
    rng = np.random.default_rng()
    mat = rng.integers(10, size=(n+1,level,n_probs))
    mask = np.array([10**i0 for i0 in range(level-1,-1,-1)]).reshape([1,level])
    for i0 in range(n_probs):
        mat[:,:,i0] = mat[:,:,i0]*mask
    
    return mat


def intMultNumLevel(level,n,n_probs): # Returns the set of problems for this level
    rng = np.random.default_rng()
    mat_0 = rng.integers(10, size=(level,n_probs))
    mat_1 = rng.integers(2, high = 9, size=(n+1,n_probs))
    
    mask = np.array([10**i0 for i0 in range(level-1,-1,-1)]).reshape([1,level])
    for i0 in range(n_probs):
        mat_0[:,i0] = mat_0[:,i0]*mask
    
    mask = np.array([10**i0 for i0 in range(n,-1,-1)]).reshape([1,n+1])
    for i0 in range(n_probs):
        mat_1[:,i0] = mat_1[:,i0]*mask
    
    return [mat_0,mat_1]


def intNumPolynomial(level,n,n_probs,ranges): # Returns the set of problems for this level
    rng = np.random.default_rng()
#    mat = rng.integers(ranges, size=(n,level,n_probs))
    mat = rng.integers(ranges, size=(n,level,n_probs))
#    variables = [Symbol('x_'+str(i0)) for i0 in range(self.n)]
    
    mat_ = []
    for i0 in range(len(mat[:,0,0])):
#        x = Symbol('x_'+str(i0))
        mat_.append( mat[i0,:,:]*Symbol('x_'+str(i0)) )
    
    mat = np.reshape(mat_,list(mat.shape))
    
    return mat

def intMultNumPolynomial(level,n,n_probs,exponentials,ranges): # Returns the set of problems for this level
    rng = np.random.default_rng()
    mat_0 = rng.integers(10, size=(level,n_probs))
    mat_0_p = rng.integers(0, high=exponentials+1, size=(level,n_probs))
    mat_1 = rng.integers(2, high = 9, size=(n,n_probs))
    mat_1_p = rng.integers(0, high=exponentials+1, size=(n+1,n_probs))
    
    mat_0_ = []
    for i0 in range(len(mat_0[:,0])):
        temp = Symbol('x_'+str(i0))**mat_0_p[i0,:]
        mat_0_.append( mat_0[i0,:]*temp )
    
    mat_0 = np.reshape(mat_0_,list(mat_0.shape))
    
    mat_1_ = []
    for i0 in range(len(mat_1[:,0])):
        temp = Symbol('x_'+str(i0))**mat_1_p[i0,:]
        mat_1_.append( mat_1[i0,:]*temp )
    
    mat_1 = np.reshape(mat_1_,list(mat_1.shape))
    
    return [mat_0,mat_1]

def intMultNumPolynomialDer(level,n,n_probs,exponentials,ranges): # Returns the set of problems for this level
    rng = np.random.default_rng()
    mat_0 = rng.integers(1, high=10, size=(level,n_probs))
    mat_0_p = rng.integers(1, high=exponentials+1, size=(level,n_probs))
    mat_1 = rng.integers(2, high = 9, size=(n,n_probs))
    mat_1_p = rng.integers(1, high=exponentials+1, size=(n+1,n_probs))
    
    mat_0_ = []
    for i0 in range(len(mat_0[:,0])):
        temp = Symbol('x_'+str(i0))**mat_0_p[i0,:]
        mat_0_.append( mat_0[i0,:]*temp )
    
    mat_0 = np.reshape(mat_0_,list(mat_0.shape))
    
    mat_1_ = []
    for i0 in range(len(mat_1[:,0])):
        temp = Symbol('x_'+str(i0))**mat_1_p[i0,:]
        mat_1_.append( mat_1[i0,:]*temp )
    
    mat_1 = np.reshape(mat_1_,list(mat_1.shape))
    
    return [mat_0,mat_1]

level = 6
n = 4
#n = 1
exponentials = 3
n_probs = 25
ranges_ = 11

#mat_0,mat_1 = intMultNumPolynomial(level,n,n_probs,exponentials,ranges_) # Returns the set of problems for this level
mat = intNumPolynomial(level,n,n_probs,ranges_) # Returns the set of problems for this level

def changeLevelN(n_page,level,n):
    if ((n_page > 2) and ( (n_page % 2) > 0 )):
        level = level + 1

    if ((n_page > 4) and ( (n_page % 4) == 0 )):
        n = n + 1
        level = level - 4
    return n_page,level,n

def saveData(level,n,problem,n_page,PATH):
    
    settings = {}
    
    settings['level'] = level
    settings['n'] = n
    settings['problem'] = problem
    settings['n_page'] = n_page
    
    np.save(PATH+'settings', [settings], allow_pickle=True)



# =============================================================================
# %% Defs Latex
# =============================================================================



def headerExercisese(doc):
    with doc.create(Section('Derivadas')):
        doc.preamble.append(Command('usepackage', 'multicol'))
        doc.append(NoEscape(r"\pagenumbering{gobble}"))
        doc.append('Resolver todas las derivadas por la definicion de limites.')
        doc.append(italic('###################'))
        doc.append(NoEscape(r"\\"))
        doc.append(NoEscape(r"\centerline{\rule{13cm}{0.4pt}}"))
#        doc.append(NoEscape(r"\textcolor[RGB]{0,0,220}{\rule{\linewidth}{0.2pt}}"))
        doc.append(NoEscape(r'\begin{multicols}{2}'))
        doc.append(NoEscape(r"\begin{enumerate}"))

        
#        with doc.create(Subsection('A subsection')):
#            doc.append('Also some crazy characters: $&#{}')


def fill_document(doc):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Section('A section')):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')


#if __name__ == '__main__':
#    # Basic document
#    doc = Document('basic')
#    fill_document(doc)
#
#    doc.generate_pdf(clean_tex=False)
#    doc.generate_tex(filepath=exercises_PATH)
#
#    # Document with `\maketitle` command activated
#    doc = Document()
#
#    doc.preamble.append(Command('title', 'Awesome Title'))
#    doc.preamble.append(Command('author', 'Anonymous author'))
#    doc.preamble.append(Command('date', NoEscape(r'\today')))
#    doc.append(NoEscape(r'\maketitle'))
#
#    fill_document(doc)
#
#    doc.generate_pdf('basic_maketitle', clean_tex=False)
#
#    # Add stuff to the document
#    with doc.create(Section('A second section')):
#        doc.append('Some text.')
#
#    doc.generate_pdf('basic_maketitle2', clean_tex=False)
#    tex = doc.dumps()  # The document as string in LaTeX syntax


# =============================================================================
# %% Class
# =============================================================================

class sumLevel():
    def __init__(self):
        
        # A Part of the problems: Add two levels after every Page
        # B Part of the problems: Add one n every two levels

        self.PATH = PATH+'/Addition/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 5
            self.n = 1
            self.problem = {}
            self.n_probs = 15
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.n_probs = 15
            
    def process(self):
        settings = {}
        mat = intNumLevel(self.level,self.n,self.n_probs)
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        self.problem[idx] = {'problems':mat,'results':[]}
        results = []
        for i0 in range(self.n_probs):
            mat_tmp = np.sum(mat[:,:,i0],axis=1)
            print('\n')
            for i1 in range(len(mat_tmp)):
                print('  ' + str('{:,}'.format(mat_tmp[i1])).zfill(self.level)+'\r')
                if (i1 < len(mat_tmp)-1):
                    print('+')
                else:
                    print('_'*(self.level+3))
            right_format = False
            tick = time()
            while not right_format:
                try:
                    x = int(input('Answer: '))
                    right_format = True
                except:
                    right_format = False
            tock = time()-tick
            if x == sum(mat_tmp):
                results.append([True, tock])
                print('Right')
            else:
                results.append([False, x, tock])
                print('Wrong \n')
                print('Solution: ' + str(sum(mat_tmp)))
                
            if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                winsound.Beep(150, 100)
                sleep(45)

        a = 0
        self.n_page,self.level,self.n = changeLevelN(self.n_page,self.level,self.n)
        
        self.problem[idx] = {'problems':mat,'results':results,'datetime':str(datetime.datetime.now())}
        
        self.n_page = self.n_page + 1
        
#        settings['level'] = self.level
#        settings['n'] = self.n
#        settings['problem'] = self.problem
#        settings['n_page'] = self.n_page
#        
#        np.save(self.PATH+'settings', [settings], allow_pickle=True)
        
        saveData(self.level,self.n,self.problem,self.n_page,self.PATH)
        
        
#        def changeLevelN(self):
#            if ((self.n_page > 2) and ( (self.n_page % 2) > 0 )):
#                self.level = self.level + 1
#    
#            if ((self.n_page > 4) and ( (self.n_page % 4) == 0 )):
#                self.n = self.n + 1
#                self.level = self.level - 4

#------------------------------------------------------------------------------

class substractionLevel():
    def __init__(self):
        
        # A Part of the problems: Add two levels after every Page
        # B Part of the problems: Add one n every two levels

        self.PATH = PATH+'/Substraction/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 5
            self.n = 1
            self.problem = {}
            self.n_probs = 15
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.n_probs = 15
            
            
    def process(self):
        settings = {}
        mat = intNumLevel(self.level,self.n,self.n_probs)
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        self.problem[idx] = {'problems':mat,'results':[]}
        results = []
        for i0 in range(self.n_probs):
            mat_tmp = np.sum(mat[:,:,i0],axis=1)
            rng = np.random.default_rng()
            sign = rng.integers(2, size=(self.n,self.n_probs))
            print('\n')
            for i1 in range(len(mat_tmp)):
                
#                print('\n')
#                print('  ' + str(mat_tmp[i1]).zfill(self.level)+'\r')
                if (i1 < len(mat_tmp)-1):
                    if sign[0][i1] > 0:
                        mat_tmp[i1] = -1*mat_tmp[i1]
#                        print('-')
#                    else:
#                    print('+')
                    if ( len(str(mat_tmp[i1]).zfill(self.level)) > self.level ):
                        print(' ' + str('{:,}'.format(mat_tmp[i1])).zfill(self.level)+'\r')
                    else:
                        print('  ' + str('{:,}'.format(mat_tmp[i1])).zfill(self.level)+'\r')
                    print('+')
                    
                else:
                    print('  ' + str('{:,}'.format(mat_tmp[i1])).zfill(self.level)+'\r')
                    print('_'*(self.level+3))
            right_format = False
            tick = time()
            while not right_format:
                try:
                    x = int(input('Answer: '))
                    right_format = True
                except:
                    right_format = False
            tock = time()-tick
            if x == sum(mat_tmp):
                results.append([True, tock])
                print('Right')
            else:
                results.append([False, x, tock])
                print('Wrong \n')
                print('Solution: ' + str(sum(mat_tmp)))
                
            if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                winsound.Beep(150, 100)
                sleep(45)
                

        a = 0
#        if ((self.n_page > 2) and ( (self.n_page % 2) > 0 )):
#            self.level =+ 1
#
#        if ((self.n_page > 2) and ( (self.n_page % 4) == 0 )):
#            self.n =+ 1
        
        self.n_page,self.level,self.n = changeLevelN(self.n_page,self.level,self.n)
        
        
        self.n_page = self.n_page + 1
        self.problem[idx] = {'problems':mat,'results':results,'datetime':str(datetime.datetime.now())}
        
        
        saveData(self.level,self.n,self.problem,self.n_page,self.PATH)
        
#------------------------------------------------------------------------------

class MultiplicationLevel():
    def __init__(self):
        
        # A Part of the problems: Add two levels after every Page
        # B Part of the problems: Add one n every two levels

        self.PATH = PATH+'/Multiplication/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 3
            self.n = 0
            self.problem = {}
            self.n_probs = 25
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.n_probs = 15
            
    def process(self):
        settings = {}
        mat = intMultNumLevel(self.level,self.n,self.n_probs)
        mat0, mat1 = mat
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        self.problem[idx] = {'problems':mat,'results':[]}
        results = []
        
        for i0 in range(self.n_probs):
            mat_tmp_0 = np.sum(mat0[:,i0],axis=0)
            mat_tmp_1 = np.sum(mat1[:,i0],axis=0)
            
            print('\n')

            print('  ' + str('{:,}'.format(mat_tmp_0)).zfill(self.level)+'\r')
            
            print('*')
            
            print('  ' + ' '*(self.level-(self.n+1)) + str('{:,}'.format(mat_tmp_1)).zfill(self.n+1)+'\r')
            
            print('_'*(self.level+3))

            right_format = False
            tick = time()
            
            while not right_format:
                try:
                    x = int(input('Answer: '))
                    right_format = True
                except:
                    right_format = False
            tock = time()-tick
            if x == (mat_tmp_0*mat_tmp_1):
                results.append([True, tock])
                print('Right')
            else:
                results.append([False, x, tock])
                print('Wrong \n')
                print('Solution: ' + str(mat_tmp_0*mat_tmp_1))
                
            if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                winsound.Beep(150, 100)
                sleep(45)
                

        self.n_page,self.level,self.n = changeLevelN(self.n_page,self.level,self.n)
        
        self.n_page = self.n_page + 1
        self.problem[idx] = {'problems':mat,'results':results,'datetime':str(datetime.datetime.now())}
        
        saveData(self.level,self.n,self.problem,self.n_page,self.PATH)

class DivLevel():
    def __init__(self):
        
        # A Part of the problems: Add two levels after every Page
        # B Part of the problems: Add one n every two levels

        self.PATH = PATH+'/Div/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 3
            self.n = 0
            self.problem = {}
            self.n_probs = 25
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            settings['n_probs'] = self.n_probs
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.n_probs = settings['n_probs']
            
    def process(self):
        settings = {}
        mat = intMultNumLevel(self.level,self.n,self.n_probs)
        mat0, mat1 = mat
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        self.problem[idx] = {'problems':mat,'results':[]}
        results = []
        
        for i0 in range(self.n_probs):
            mat_tmp_0 = np.sum(mat0[:,i0],axis=0)
            mat_tmp_1 = np.sum(mat1[:,i0],axis=0)
            
            print('\n')

            print('  '  + ' '*(self.n+1) + str('{:,}'.format(mat_tmp_0)).zfill(self.level)+'\r')
            
            print('/')
            
            print('  ' + str('{:,}'.format(mat_tmp_1)).zfill(self.n+1)+'\r')
            
            print('_'*(self.level+3))

            right_format = False
            tick = time()
            
            while not right_format:
                try:
                    x = int(input('Answer: '))
                    right_format = True
                except:
                    right_format = False
            tock = time()-tick
            if x == int(mat_tmp_0/mat_tmp_1):
                results.append([True, tock])
                print('Right')
            else:
                results.append([False, x, tock])
                print('Wrong \n')
                print('Solution: ' + str(mat_tmp_0/mat_tmp_1))
                
            if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                winsound.Beep(150, 100)
                sleep(45)
                

        self.n_page,self.level,self.n,self.n_probs = self.changeLevelN()
        
        self.n_page = self.n_page + 1
        self.problem[idx] = {'problems':mat,'results':results,'datetime':str(datetime.datetime.now())}
        
        self.saveData()

    def changeLevelN(self):
        if ((self.n_page > 2) and ( (self.n_page % 2) > 0 )):
            self.level = self.level + 1
    
        if ((self.n_page > 4) and ( (self.n_page % 4) == 0 )):
            self.n = self.n + 1
            self.level = self.level - 4
            self.n_probs = 10
        return self.n_page,self.level,self.n,self.n_probs


    def saveData(self):
        
        settings = {}
        
        settings['level'] = self.level
        settings['n'] = self.n
        settings['problem'] = self.problem
        settings['n_page'] = self.n_page
        settings['n_probs'] = self.n_probs
        
        np.save(self.PATH+'settings', [settings], allow_pickle=True)    

# =============================================================================
# %% Algebra
# =============================================================================

class PolynomialsSum():
    def __init__(self):
        
        # A Part of the problems: Add two levels after every Page
        # B Part of the problems: Add one n every two levels

        self.PATH = PATH+'/Polynomials Addition/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 3
            self.n = 3
            self.problem = {}
            self.n_probs = 10
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.n_probs = 10
            
    def changeLevelN(self):
        if ((self.n_page > 4) and ( (self.n_page % 4) > 0 )):
            self.level = self.level + 1
    
        if ((self.n_page > 8) and ( (self.n_page % 8) == 0 )):
            self.n = self.n + 1
            self.level = self.level - 4
        return self.n_page, self.level, self.n
    
    def process(self):
        settings = {}
        mat = intNumPolynomial(self.level,self.n,self.n_probs,101)
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        self.problem[idx] = {'problems':mat,'results':[]}
        results = []
        
        rng = np.random.default_rng()
        sign = rng.integers(2, size=(self.n*self.level,self.n_probs))
        sign = (sign*2)-1
        
        for i0 in range(self.n_probs):
            
            sign_ = sign[:,i0]
            
            mat_tmp = mat[:,:,i0]
            mat_tmp_ = [mat_tmp[:,i1] for i1 in range(np.shape(mat_tmp)[1])]
            mat_tmp_ = np.reshape(mat_tmp_,[np.shape(mat_tmp)[1],np.shape(mat_tmp)[0]]).reshape([1,-1]).reshape([1,-1])
            mat_tmp_ = mat_tmp_*sign_
            mat_tmp_ = mat_tmp_[0]
            
            mat_tmp__ = []
            for i1,tmp in enumerate(sign_):
                if tmp > 0:
                    mat_tmp__.append( '+ ' + str(mat_tmp_[i1]) )
                elif tmp < 0:
                    try:
                        mat_tmp__.append( '- ' + str(mat_tmp_[i1]).split('-')[1] )
                    except:
                        a = 0
            mat_tmp__ = ' '.join(mat_tmp__)
            
#            for i1 in range(len(mat_tmp)):
#                print('  ' + str(mat_tmp[i1]).zfill(self.level)+'\r')
#                if (i1 < len(mat_tmp)-1):
#                    print('+')
#                else:
#                    print('_'*(self.level+3))
            print('Solve the Polynomial Operation: \n')
            
            print(mat_tmp__)
            
            right_format = False
            tick = time()
            while not right_format:
                try:
                    x = parse_expr(input('Answer: '))
                    right_format = True
                except:
                    right_format = False
            tock = time()-tick
            if x == np.sum(mat_tmp_):
                results.append([True, tock])
                print('Right')
            else:
                results.append([False, x, tock])
                print('Wrong \n')
                print('Solution: ' + str(sum(mat_tmp_)))
                
            if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                winsound.Beep(150, 100)
                sleep(45)

        a = 0
        self.n_page,self.level,self.n = self.changeLevelN()
        
        self.problem[idx] = {'problems':mat,'results':results, 'sign':sign_,'datetime':str(datetime.datetime.now())}
        
        self.n_page = self.n_page + 1
        
        saveData(self.level,self.n,self.problem,self.n_page,self.PATH)
        
#------------------------------------------------------------------------------

class PolynomialsOp():
    def __init__(self):
        
        # A Part of the problems: Add two levels after every Page
        # B Part of the problems: Add one n every two levels

        self.PATH = PATH+'/Polynomials Operations/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 3
            self.n = 1
            self.problem = {}
            self.n_probs = 10
            self.exponentials = 3
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['exponentials'] = self.exponentials
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.exponentials = settings['exponentials']
            self.n_probs = 10
            
    def changeLevelN(self):
        if ((self.n_page > 4) and ( (self.n_page % 4) > 0 )):
            self.level = self.level + 1
    
        if ((self.n_page > 8) and ( (self.n_page % 8) == 0 )):
            self.n = self.n + 1
            self.level = self.level - 4
            self.exponentials = self.exponentials-1
            
            
        if ((self.n_page > 3) and ( (self.n_page % 4) > 0 )):
            self.exponentials = self.exponentials + 1
        
        return self.n_page, self.level, self.n
    
    def saveData(self):
        
        settings = {}
        
        settings['level'] = self.level
        settings['n'] = self.n
        settings['problem'] = self.problem
        settings['n_page'] = self.n_page
        settings['exponentials'] = self.exponentials
        
        np.save(self.PATH+'settings', [settings], allow_pickle=True)
    
    def process(self):
        settings = {}
        mat = intMultNumPolynomial(self.level,self.n,self.n_probs,self.exponentials,101)
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        self.problem[idx] = {'problems':mat,'results':[]}
        mat_0, mat_1 = mat
        results = []
        
        rng = np.random.default_rng()
        sign_0 = rng.integers(2, size=(self.level,self.n_probs))
        sign_0 = (sign_0*2)-1
        sign_1 = rng.integers(2, size=(self.n,self.n_probs))
        sign_1 = (sign_1*2)-1
        
        print('Solve the Polynomial Operation: \n')
        
        for i0 in range(self.n_probs):
            
            mat_tmp_0 = mat_0[:,i0].reshape(1,-1)[0]
            mat_tmp_0 = mat_tmp_0*sign_0[:,i0]
            
            mat_tmp_1 = mat_1[:,i0].reshape(1,-1)[0]
            mat_tmp_1 = mat_tmp_1*sign_1[:,i0]
            
            mat_tmp_0_ = []
            for i1,tmp in enumerate(sign_0[:,i0]):
                if ( (tmp > 0) and (i1 > 0) ):
                    mat_tmp_0_.append( '+ ' + str(mat_tmp_0[i1]) )
                elif ( ( tmp < 0) and (i1 > 0) ):
                    try:
                        mat_tmp_0_.append( '- ' + str(mat_tmp_0[i1]).split('-')[1] )
                    except:
                        a=0
                        mat_tmp_0_.append( '- ' + str(mat_tmp_0[i1]) )
                else:
                    mat_tmp_0_.append( str(mat_tmp_0[i1]) )
            mat_tmp_0_ = ' '.join(mat_tmp_0_)
            
            mat_tmp_1_ = []
            for i1,tmp in enumerate(sign_1[:,i0]):
                if ( (tmp > 0) and (i1 > 0) ):
                    mat_tmp_1_.append( '+ ' + str(mat_tmp_1[i1]) )
                elif ( (tmp < 0) and (i1 > 0) ):
                    mat_tmp_1_.append( '- ' + str(mat_tmp_1[i1]).split('-')[1] )
                else:
                    mat_tmp_1_.append( str(mat_tmp_1[i1]) )
                    
            mat_tmp_1_ = ' '.join(mat_tmp_1_)
            
            mat_tmp_ = '('+mat_tmp_0_+')'+ '*' +'('+mat_tmp_1_+')'
            
            print(mat_tmp_)
            
            right_format = False
            tick = time()
            while not right_format:
                try:
                    x = parse_expr(input('Answer: '))
                    right_format = True
                except:
                    right_format = False
            tock = time()-tick
            if x == np.sum(mat_tmp_1*mat_tmp_0):
                results.append([True, tock])
                print('Right')
                print('')                
            else:
                results.append([False, x, tock])
                print('Wrong \n')
                print('Solution: ' + str(sum(mat_tmp_1*mat_tmp_0)))
                print('')
                
            if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                winsound.Beep(150, 100)
                sleep(45)

        a = 0
        self.n_page,self.level,self.n = self.changeLevelN()
        
        self.problem[idx] = {'problems':mat,'results':results,'datetime':str(datetime.datetime.now())}
        
        self.n_page = self.n_page + 1
        
        self.saveData()

#------------------------------------------------------------------------------

class PolynomialsFact():
    def __init__(self):
        
        # A Part of the problems: Add two levels after every Page
        # B Part of the problems: Add one n every two levels

        self.PATH = PATH+'/Polynomials Factorization/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 3
            self.n = 1
            self.problem = {}
            self.n_probs = 10
            self.exponentials = 3
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['exponentials'] = self.exponentials
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.exponentials = settings['exponentials']
            self.n_probs = 10
            
    def changeLevelN(self):
        if ((self.n_page > 4) and ( (self.n_page % 4) > 0 )):
            self.level = self.level + 1
    
        if ((self.n_page > 8) and ( (self.n_page % 8) == 0 )):
            self.n = self.n + 1
            self.level = self.level - 4
            self.exponentials = self.exponentials-1
            
            
        if ((self.n_page > 3) and ( (self.n_page % 4) > 0 )):
            self.exponentials = self.exponentials + 1
        
        return self.n_page, self.level, self.n
    
    def saveData(self):
        
        settings = {}
        
        settings['level'] = self.level
        settings['n'] = self.n
        settings['problem'] = self.problem
        settings['n_page'] = self.n_page
        settings['exponentials'] = self.exponentials
        
        np.save(self.PATH+'settings', [settings], allow_pickle=True)
    
    def process(self):
        settings = {}
        mat = intMultNumPolynomial(self.level,self.n,self.n_probs,self.exponentials,101)
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        self.problem[idx] = {'problems':mat,'results':[]}
        mat_0, mat_1 = mat
        results = []
        
        rng = np.random.default_rng()
        sign_0 = rng.integers(2, size=(self.level,self.n_probs))
        sign_0 = (sign_0*2)-1
        sign_1 = rng.integers(2, size=(self.n,self.n_probs))
        sign_1 = (sign_1*2)-1
        
        for i0 in range(self.n_probs):
            
            mat_tmp_0 = mat_0[:,i0].reshape(1,-1)[0]
            mat_tmp_0 = mat_tmp_0*sign_0[:,i0]
            
            mat_tmp_1 = mat_1[:,i0].reshape(1,-1)[0]
            mat_tmp_1 = mat_tmp_1*sign_1[:,i0]
            
            mat_tmp_ = mat_tmp_1*mat_tmp_0
            
            mat_tmp__ = []
            for i1,tmp in enumerate(mat_tmp_):
                if len(tmp.args)>0:
                    if ( (tmp.args[0] > 0) and (i1 > 0) ):
                        mat_tmp__.append( '+ ' + str(tmp) )
                    elif ( ( tmp.args[0] < 0) and (i1 > 0) ):
                        mat_tmp__.append( '- ' + str(tmp).split('-')[1] )
                    else:
                        mat_tmp__.append( str(tmp) )
                else:
                    if ( (tmp > 0) and (i1 > 0) ):
                        mat_tmp__.append( '+ ' + str(tmp) )
                    elif ( ( tmp < 0) and (i1 > 0) ):
                        mat_tmp__.append( '- ' + str(tmp).split('-')[1] )
                    else:
                        mat_tmp__.append( str(tmp) )
            mat_tmp__ = ' '.join(mat_tmp__)
            
            
            mat_tmp_0_ = []
            for i1,tmp in enumerate(sign_0[:,i0]):
                if ( (tmp > 0) and (i1 > 0) ):
                    mat_tmp_0_.append( '+ ' + str(mat_tmp_0[i1]) )
                elif ( ( tmp < 0) and (i1 > 0) ):
                    try:
                        mat_tmp_0_.append( '- ' + str(mat_tmp_0[i1]).split('-')[1] )
                    except:
                        a = 0
                        mat_tmp_0_.append( '- ' + str(mat_tmp_0[i1]) )
                else:
                    mat_tmp_0_.append( str(mat_tmp_0[i1]) )
            mat_tmp_0_ = ' '.join(mat_tmp_0_)
            
            mat_tmp_1_ = []
            for i1,tmp in enumerate(sign_1[:,i0]):
                if ( (tmp > 0) and (i1 > 0) ):
                    mat_tmp_1_.append( '+ ' + str(mat_tmp_1[i1]) )
                elif ( (tmp < 0) and (i1 > 0) ):
                    mat_tmp_1_.append( '- ' + str(mat_tmp_1[i1]).split('-')[1] )
                else:
                    mat_tmp_1_.append( str(mat_tmp_1[i1]) )
                    
            mat_tmp_1_ = ' '.join(mat_tmp_1_)
            
            mat_tmp___ = '('+mat_tmp_0_+')'+ '*' +'('+mat_tmp_1_+')'
            
            print('Solve the Polynomial Operation: \n')
            
            print(mat_tmp__)
            
            right_format = False
            tick = time()
            while not right_format:
                try:
                    x = parse_expr(input('Answer: '))
                    right_format = True
                except:
                    right_format = False
            tock = time()-tick
            if spy.expand(x) == np.sum(mat_tmp_1*mat_tmp_0):
                results.append([True, tock])
                print('Right')
            else:
                results.append([False, x, tock])
                print('Wrong \n')
                print('Solution: ' + str(mat_tmp___))
                
            if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                winsound.Beep(150, 100)
                sleep(45)

        a = 0
        self.n_page,self.level,self.n = self.changeLevelN()
        
        self.problem[idx] = {'problems':mat,'results':results,'datetime':str(datetime.datetime.now())}
        
        self.n_page = self.n_page + 1
        
        self.saveData()

#------------------------------------------------------------------------------

class EqSystems():
    def __init__(self):
        
        # A Part of the problems: Add two levels after every Page
        # B Part of the problems: Add one n every two levels

        self.PATH = PATH+'/Simultaneous Equations/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 2
            self.n = 1
            self.problem = {}
            self.n_probs = 5
            self.exponentials = 1
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['exponentials'] = self.exponentials
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.exponentials = settings['exponentials']
            self.n_probs = 5
            
    def changeLevelN(self):
        if ((self.n_page > 4) and ( (self.n_page % 4) > 0 )):
            self.level = self.level + 1
    
        if ((self.n_page > 8) and ( (self.n_page % 8) == 0 )):
            self.n = self.n + 1
            self.level = self.level - 4
        
        return self.n_page, self.level, self.n
    
    def process(self):
        settings = {}
        mat_0 = intNumPolynomial(self.level,self.level,self.n_probs,101)
        mat_0 = mat_0.reshape([self.level,self.level,self.n_probs])
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        results = []

        rng = np.random.default_rng()
        mat_1 = rng.integers(11, size=(self.level,self.n_probs))
        
        sign_0 = rng.integers(2, size=(self.level*self.level,self.n_probs))
        sign_0 = (sign_0*2)-1
        sign_0 = sign_0.reshape(mat_0.shape)
        sign_1 = rng.integers(2, size=(self.level,self.n_probs))
        sign_1 = (sign_1*2)-1
        
        mat_0 = mat_0*sign_0
        
        x_ = []
        for tmp in mat_0[:,0,:]:
            for tmp_ in tmp:
                try:
                    x_.append(tmp_.args[1])
                except:
                    a = 0
        x_ = set(x_)
        x_ = list(x_)
        
#        print(mat_0[:,:,0])
#        print(mat_1[:,0])
#        print(np.sum(mat_0[:,:,0],axis=1))
        Y = []
        Y_ = []
        
        mat_1 = mat_1*sign_1
        
        for n_ in range(self.n_probs):
            mat_0[:,:,n_] = mat_0[:,:,n_].transpose()
            tmp = mat_0[:,:,n_]
            Y_ = []
            for i0 in range(self.level):
#                if len(tmp[i0].args) > 0:
#                print(tmp[i0].subs(tmp[i0].args[1],mat_1[i0,n_]*sign_1[i0,n_]))
                Y__ = []
                for i1 in range(self.level):
                    if len(tmp[i0][i1].args) > 0:
                        Y__.append(tmp[i0][i1].subs(tmp[i0][i1].args[1],mat_1[i1,n_]))
                    else:
                        tmp[i0][i1] = 0
                        Y__.append(0)
                Y_.append(sum(Y__))
            Y.append(Y_)

        
        Y = np.asarray(Y)
        
        self.problem[idx] = {'problems':[mat_0,mat_1,sign_0,sign_1, Y],'results':[]}
        
        for i0 in range(self.n_probs):
            
            mat_tmp_0_0 = mat_0[:,:,i0].reshape(self.level,self.level)[0]
#            mat_tmp_0 = mat_tmp_0*sign_0[:2,i0]
            
#            mat_tmp_1 = mat_1[:,i0].reshape(1,-1)
#            mat_tmp_1 = mat_tmp_1*sign_0[:2,i0]
            mat_tmp_1 = mat_1[:,i0]
            
            mat_tmp_0_0_ = []
            mat_tmp_0_0__ = []
            for i1, mat_tmp_0_0 in enumerate(mat_0[:,:,i0]):
                mat_tmp_0_0__ = []
                for i2,tmp in enumerate(mat_tmp_0_0):
                    try:
                        if len(tmp.args) > 0:
                            if ( (tmp.args[0] > 0) and (i2 > 0) ):
                                mat_tmp_0_0__.append( '+ ' + str(mat_tmp_0_0[i2]) )
                            elif ( ( tmp.args[0] < 0) and (i2 > 0) ):
                                mat_tmp_0_0__.append( '- ' + str(mat_tmp_0_0[i2]).split('-')[1] )
                            else:
                                mat_tmp_0_0__.append( str(mat_tmp_0_0[i2]) )
                        else:
                            mat_tmp_0_0__.append( str(mat_tmp_0_0[i2]) )
                    except:
                        print('Error')
                        print(tmp)
                        len(tmp.args)
                mat_tmp_0_0_.append(' '.join(mat_tmp_0_0__) + ' = ' + str(Y[i0,i1]))
            
            mat_tmp_1_ = {}
            for i1,tmp in enumerate(mat_tmp_1):
                mat_tmp_1_['x_'+str(i1)] = tmp
            
#            mat_tmp_1_ = ' '.join(mat_tmp_1_)
#            
#            mat_tmp_ = '('+mat_tmp_0_+')'+ '*' +'('+mat_tmp_1_+')'
            
            print('Solve the Matrix: \n')
            
#            print(mat_tmp_)
            
            for i1, mat_tmp_0_0__ in enumerate(mat_tmp_0_0_):
                print(mat_tmp_0_0__)
                
            answers = 0
            sol = []
            right_format = False
            tick = time()
            x__ = x_.copy()
            results_ = []
            tock = 0
            while ((not right_format) or (answers < self.level)):
                try:
#                    x = parse_expr(input('Answer: '))
                    x = input('Answer: ')
                    x = x.split('=')
                    x = [parse_expr(x_.strip()) for x_ in x]
                    tmp = 0
                    tmp_ = None
                    try:
                        x[0] = int(x[0])
                        tmp = tmp+1
                        tmp_ = 1
                    except:
                        tmp = tmp
                    try:
                        x[1] = int(x[1])
                        tmp = tmp+1
                        tmp_ = 0
                    except:
                        tmp = tmp
                    
                    idx = []
                    for i0, x___ in enumerate(x__):
                        if x[tmp-1] == x___:
                            idx.append(i0)

                    if len(idx) == 1:
                        del x__[idx[0]]
                    else:
                        del i45
                    
                    if ((len(x) == 2) and (tmp == 1)):
                        if x[tmp_] in x_:
                            right_format = True
                            answers = answers + 1
                            sol.append([x[tmp_], x[tmp_-1]])
                            if mat_tmp_1_[str(x[tmp_])] == x[tmp_-1]:
                                print('Right')
                                tock = time()-tick-tock
                                results_.append([True, tock])
                                print('')
                            else:
                                print('wrong \n')
                                print(str(x[tmp_]) + ' = ' + str(mat_tmp_1_[str(x[tmp_])]))
                                tock = time()-tick-tock
                                results_.append([False, tock])
                                print('')
                except:
                    right_format = False
            
            results.append(np.asanyarray(results_))
            if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                winsound.Beep(150, 100)
                sleep(45)

        a = 0
        results = np.asarray(results)
        self.n_page,self.level,self.n = self.changeLevelN()
        
        self.problem[idx] = {'problems':[mat_0,mat_1,sign_0,sign_1, Y],'results':results,'datetime':str(datetime.datetime.now())}
        
        self.n_page = self.n_page + 1
        
        saveData(self.level,self.n,self.problem,self.n_page,self.PATH)

# =============================================================================
# %% Calculus
# =============================================================================

class DerivativesLevel():
    def __init__(self,printed_exercises=False):
        
        # after adding one level start to add/sumbstract more terms
        #   if n%2 add another term
        # after two levels generate more complex functions

        self.PATH = PATH+'/Derivatives/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 1
            self.n = 1
            self.problem = {}
            self.n_probs = 20
            self.exponentials = 3
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['exponentials'] = self.exponentials
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.exponentials = settings['exponentials']
            self.n_probs = 20
            
        self.printed_exercises = printed_exercises
        if self.printed_exercises:
            self.doc = Document('basic')
            headerExercisese(self.doc)
#            

            
            self.path_now = os.getcwd()
#            os.chdir(exercises_PATH)
#            self.doc.generate_pdf(clean_tex=False)
#            self.doc.generate_tex(filepath=exercises_PATH)
            os.chdir(self.path_now)
        
    def changeLevelN(self):
        if ((self.n_page > 4) and ( (self.n_page % 4) > 0 )):
            self.level = self.level + 1
    
        if ((self.n_page > 8) and ( (self.n_page % 8) == 0 )):
            self.n = self.n + 1
            self.level = self.level - 4
            self.exponentials = self.exponentials-1
            
            
        if ((self.n_page > 3) and ( (self.n_page % 4) > 0 )):
            self.exponentials = self.exponentials + 1
        
        return self.n_page, self.level, self.n
    
    def saveData(self):
        
        settings = {}
        
        settings['level'] = self.level
        settings['n'] = self.n
        settings['problem'] = self.problem
        settings['n_page'] = self.n_page
        settings['exponentials'] = self.exponentials
        
        np.save(self.PATH+'settings', [settings], allow_pickle=True)
    
    def process(self):
        settings = {}
        mat = intMultNumPolynomialDer(self.level,self.n,self.n_probs,self.exponentials,11)
        #Dictionary of functions
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        self.problem[idx] = {'problems':mat,'results':[]}
        mat_0, mat_1 = mat
        results = []
        
        rng = np.random.default_rng()
        sign_0 = rng.integers(2, size=(self.level,self.n_probs))
        sign_0 = (sign_0*2)-1
        sign_1 = rng.integers(2, size=(self.n,self.n_probs))
        sign_1 = (sign_1*2)-1
        
        for i0 in range(self.n_probs):
            
            mat_tmp_0 = mat_0[:,i0].reshape(1,-1)[0]
            mat_tmp_0 = mat_tmp_0*sign_0[:,i0]
            
            mat_tmp_1 = mat_1[:,i0].reshape(1,-1)[0]
            mat_tmp_1 = mat_tmp_1*sign_1[:,i0]
            
            mat_tmp_ = mat_tmp_1*mat_tmp_0
            
            mat_tmp__ = []
            for i1,tmp in enumerate(mat_tmp_):
                if len(tmp.args)>0:
                    if ( (tmp.args[0] > 0) and (i1 > 0) ):
                        mat_tmp__.append( '+ ' + str(tmp) )
                    elif ( ( tmp.args[0] < 0) and (i1 > 0) ):
                        mat_tmp__.append( '- ' + str(tmp).split('-')[1] )
                    else:
                        mat_tmp__.append( str(tmp) )
                else:
                    if ( (tmp > 0) and (i1 > 0) ):
                        mat_tmp__.append( '+ ' + str(tmp) )
                    elif ( ( tmp < 0) and (i1 > 0) ):
                        mat_tmp__.append( '- ' + str(tmp).split('-')[1] )
                    else:
                        mat_tmp__.append( str(tmp) )
            mat_tmp__ = ' '.join(mat_tmp__)
            
            
            mat_tmp_0_ = []
            for i1,tmp in enumerate(sign_0[:,i0]):
                if ( (tmp > 0) and (i1 > 0) ):
                    mat_tmp_0_.append( '+ ' + str(mat_tmp_0[i1]) )
                elif ( ( tmp < 0) and (i1 > 0) ):
                    try:
                        mat_tmp_0_.append( '- ' + str(mat_tmp_0[i1]).split('-')[1] )
                    except:
                        a = 0
                        mat_tmp_0_.append( '- ' + str(mat_tmp_0[i1]) )
                else:
                    mat_tmp_0_.append( str(mat_tmp_0[i1]) )
            mat_tmp_0_ = ' '.join(mat_tmp_0_)
            #mat_tmp_0_ = spy.Derivative(mat_tmp_0_)
            
            mat_tmp_1_ = []
            for i1,tmp in enumerate(sign_1[:,i0]):
                if ( (tmp > 0) and (i1 > 0) ):
                    mat_tmp_1_.append( '+ ' + str(mat_tmp_1[i1]) )
                elif ( (tmp < 0) and (i1 > 0) ):
                    mat_tmp_1_.append( '- ' + str(mat_tmp_1[i1]).split('-')[1] )
                else:
                    mat_tmp_1_.append( str(mat_tmp_1[i1]) )
                    
            mat_tmp_1_ = ' '.join(mat_tmp_1_)
            #mat_tmp_1_ = spy.Derivative(mat_tmp_1_)
            
            mat_tmp___ = '('+mat_tmp_0_+')'+ '*' +'('+mat_tmp_1_+')'
            
            
            
            if self.printed_exercises:
                temp = mat_tmp_1*mat_tmp_0
                formula = latex(spy.Derivative(temp[0], temp[0].args[-1].args[0]))
#                self.doc.append(NoEscape(r'\begin{equation}'))
                self.doc.append(NoEscape(r"\item"+'$'+NoEscape(str(formula))+'$'))
                self.doc.append(NoEscape(r"\bigskip"))
                self.doc.append(NoEscape(r"\bigskip"))
                self.doc.append(NoEscape(r"\bigskip"))
                

#                self.doc.append(NoEscape(str(formula)))
#                self.doc.append(NoEscape(r'\end{equation}'))
            else:
                print('Find the derivative with respecto to x_0: \n')
                
                try:
                    temp = mat_tmp_1*mat_tmp_0
                    print(spy.Derivative(temp[0], temp[0].args[-1].args[0]))
                except:
                    print(mat_tmp__)
                
                right_format = False
                tick = time()
                while not right_format:
                    try:
                        x = parse_expr(input('Answer: '))
                        right_format = True
                    except:
                        right_format = False
                tock = time()-tick
                temp = mat_tmp_1*mat_tmp_0
                if x == spy.Derivative(temp[0]).doit():
                    results.append([True, tock])
                    print('Right')
                    print('')
                else:
                    results.append([False, x, tock])
                    print('Wrong \n')
                    print('Solution: ' + str(mat_tmp___))
                    print('')
                    
                if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                    winsound.Beep(150, 100)
                    sleep(45)
                
        
        if self.printed_exercises:
            a = 0
            self.doc.append(NoEscape(r"\end{enumerate}"))
            self.doc.append(NoEscape(r'\end{multicols}'))
            os.chdir(exercises_PATH)
            self.doc.generate_pdf(clean_tex=False)
            os.chdir(self.path_now)
        else:
            a = 0
            self.n_page,self.level,self.n = self.changeLevelN()
            
            self.problem[idx] = {'problems':mat,'results':results,'datetime':str(datetime.datetime.now())}
            
            self.n_page = self.n_page + 1
            
            self.saveData()

#------------------------------------------------------------------------------


class IntegralsLevel():
    def __init__(self,printed_exercises=False):
        
        # after adding one level start to add/sumbstract more terms
        #   if n%2 add another term
        # after two levels generate more complex functions

        self.PATH = PATH+'/Integrals/'
        try:
            os.mkdir(self.PATH)
            
            self.level = 1
            self.n = 1
            self.problem = {}
            self.n_probs = 20
            self.exponentials = 3
            
            self.n_page = 1
            
            settings = {}
            
            settings['level'] = self.level
            settings['n'] = self.n
            settings['exponentials'] = self.exponentials
            settings['problem'] = self.problem
            settings['n_page'] = self.n_page
            
            np.save(self.PATH+'settings', [settings], allow_pickle=True)
        except:
            # Load hist
            
            settings = np.load(self.PATH+'settings.npy', allow_pickle=True)
            settings = list(settings)
            settings = settings[0]
            
            self.level = settings['level']
            self.n = settings['n']
            self.problem = settings['problem']
            self.n_page = settings['n_page']
            self.exponentials = settings['exponentials']
            self.n_probs = 20
            
        self.printed_exercises = printed_exercises
        if self.printed_exercises:
            self.doc = Document('basic')
            headerExercisese(self.doc)
#            

            
            self.path_now = os.getcwd()
#            os.chdir(exercises_PATH)
#            self.doc.generate_pdf(clean_tex=False)
#            self.doc.generate_tex(filepath=exercises_PATH)
            os.chdir(self.path_now)
        
    def changeLevelN(self):
        if ((self.n_page > 4) and ( (self.n_page % 4) > 0 )):
            self.level = self.level + 1
    
        if ((self.n_page > 8) and ( (self.n_page % 8) == 0 )):
            self.n = self.n + 1
            self.level = self.level - 4
            self.exponentials = self.exponentials-1
            
            
        if ((self.n_page > 3) and ( (self.n_page % 4) > 0 )):
            self.exponentials = self.exponentials + 1
        
        return self.n_page, self.level, self.n
    
    def saveData(self):
        
        settings = {}
        
        settings['level'] = self.level
        settings['n'] = self.n
        settings['problem'] = self.problem
        settings['n_page'] = self.n_page
        settings['exponentials'] = self.exponentials
        
        np.save(self.PATH+'settings', [settings], allow_pickle=True)
    
    def process(self):
        settings = {}
        mat = intMultNumPolynomialDer(self.level,self.n,self.n_probs,self.exponentials,11)
        #Dictionary of functions
        idx = 'level_'+str(self.level)+'-n'+str(self.n)+'nPage'+str(self.n_page)
        self.problem[idx] = {'problems':mat,'results':[]}
        mat_0, mat_1 = mat
        results = []
        
        rng = np.random.default_rng()
        sign_0 = rng.integers(2, size=(self.level,self.n_probs))
        sign_0 = (sign_0*2)-1
        sign_1 = rng.integers(2, size=(self.n,self.n_probs))
        sign_1 = (sign_1*2)-1
        
        for i0 in range(self.n_probs):
            
            mat_tmp_0 = mat_0[:,i0].reshape(1,-1)[0]
            mat_tmp_0 = mat_tmp_0*sign_0[:,i0]
            
            mat_tmp_1 = mat_1[:,i0].reshape(1,-1)[0]
            mat_tmp_1 = mat_tmp_1*sign_1[:,i0]
            
            mat_tmp_ = mat_tmp_1*mat_tmp_0
            
            mat_tmp__ = []
            for i1,tmp in enumerate(mat_tmp_):
                if len(tmp.args)>0:
                    if ( (tmp.args[0] > 0) and (i1 > 0) ):
                        mat_tmp__.append( '+ ' + str(tmp) )
                    elif ( ( tmp.args[0] < 0) and (i1 > 0) ):
                        mat_tmp__.append( '- ' + str(tmp).split('-')[1] )
                    else:
                        mat_tmp__.append( str(tmp) )
                else:
                    if ( (tmp > 0) and (i1 > 0) ):
                        mat_tmp__.append( '+ ' + str(tmp) )
                    elif ( ( tmp < 0) and (i1 > 0) ):
                        mat_tmp__.append( '- ' + str(tmp).split('-')[1] )
                    else:
                        mat_tmp__.append( str(tmp) )
            mat_tmp__ = ' '.join(mat_tmp__)
            
            
            mat_tmp_0_ = []
            for i1,tmp in enumerate(sign_0[:,i0]):
                if ( (tmp > 0) and (i1 > 0) ):
                    mat_tmp_0_.append( '+ ' + str(mat_tmp_0[i1]) )
                elif ( ( tmp < 0) and (i1 > 0) ):
                    try:
                        mat_tmp_0_.append( '- ' + str(mat_tmp_0[i1]).split('-')[1] )
                    except:
                        a = 0
                        mat_tmp_0_.append( '- ' + str(mat_tmp_0[i1]) )
                else:
                    mat_tmp_0_.append( str(mat_tmp_0[i1]) )
            mat_tmp_0_ = ' '.join(mat_tmp_0_)
            #mat_tmp_0_ = spy.Derivative(mat_tmp_0_)
            
            mat_tmp_1_ = []
            for i1,tmp in enumerate(sign_1[:,i0]):
                if ( (tmp > 0) and (i1 > 0) ):
                    mat_tmp_1_.append( '+ ' + str(mat_tmp_1[i1]) )
                elif ( (tmp < 0) and (i1 > 0) ):
                    mat_tmp_1_.append( '- ' + str(mat_tmp_1[i1]).split('-')[1] )
                else:
                    mat_tmp_1_.append( str(mat_tmp_1[i1]) )
                    
            mat_tmp_1_ = ' '.join(mat_tmp_1_)
            #mat_tmp_1_ = spy.Derivative(mat_tmp_1_)
            
            mat_tmp___ = '('+mat_tmp_0_+')'+ '*' +'('+mat_tmp_1_+')'
            
            
            
            if self.printed_exercises:
                temp = mat_tmp_1*mat_tmp_0
                formula = latex(spy.Derivative(temp[0], temp[0].args[-1].args[0]))
#                self.doc.append(NoEscape(r'\begin{equation}'))
                self.doc.append(NoEscape(r"\item"+'$'+NoEscape(str(formula))+'$'))
                self.doc.append(NoEscape(r"\bigskip"))
                self.doc.append(NoEscape(r"\bigskip"))
                self.doc.append(NoEscape(r"\bigskip"))
                

#                self.doc.append(NoEscape(str(formula)))
#                self.doc.append(NoEscape(r'\end{equation}'))
            else:
                print('Find the derivative with respecto to x_0: \n')
                
                try:
                    temp = mat_tmp_1*mat_tmp_0
                    print(spy.Derivative(temp[0], temp[0].args[-1].args[0]))
                except:
                    print(mat_tmp__)
                
                right_format = False
                tick = time()
                while not right_format:
                    try:
                        x = parse_expr(input('Answer: '))
                        right_format = True
                    except:
                        right_format = False
                tock = time()-tick
                temp = mat_tmp_1*mat_tmp_0
                if x == spy.Derivative(temp[0]).doit():
                    results.append([True, tock])
                    print('Right')
                    print('')
                else:
                    results.append([False, x, tock])
                    print('Wrong \n')
                    print('Solution: ' + str(mat_tmp___))
                    print('')
                    
                if ( (i0 == self.n_probs-1) or (i0 == int(self.n_probs/2))):
                    winsound.Beep(150, 100)
                    sleep(45)
                
        
        if self.printed_exercises:
            a = 0
            self.doc.append(NoEscape(r"\end{enumerate}"))
            self.doc.append(NoEscape(r'\end{multicols}'))
            os.chdir(exercises_PATH)
            self.doc.generate_pdf(clean_tex=False)
            os.chdir(self.path_now)
        else:
            a = 0
            self.n_page,self.level,self.n = self.changeLevelN()
            
            self.problem[idx] = {'problems':mat,'results':results,'datetime':str(datetime.datetime.now())}
            
            self.n_page = self.n_page + 1
            
            self.saveData()

#------------------------------------------------------------------------------

# =============================================================================
# %% Load Modules
# =============================================================================
levelequationSystems = EqSystems()

levelFact = PolynomialsFact()

levelOp = PolynomialsOp()

levelPSum = PolynomialsSum()

levelSum = sumLevel()

levelSubs = substractionLevel()

levelMult = MultiplicationLevel()

levelDiv = DivLevel()

#levelDiffCalc = DerivativesLevel(printed_exercises = True)
levelDiffCalc = DerivativesLevel(printed_exercises = False)

#levelequationSystems.process()

levelDiffCalc.process()

# =============================================================================
# %% Decide Which Goes First
# =============================================================================
#levelPFct.process()



if (levelFact.n_page*2 < max([levelMult.n_page, levelDiv.n_page, levelPSum.n_page, levelOp.n_page])):

    levelFact.process()
#    levelequationSystems.process()
    levelDiffCalc.process()

elif (levelPSum.n_page*2 < max([levelSum.n_page, levelSubs.n_page])):
    
    levelMult.process()

    levelDiv.process()
    
    levelPSum.process()
    
    levelOp.process()

elif (levelPSum.n_page*2 >= max([levelSum.n_page, levelSubs.n_page])):
    
    levelSum.process()
    
    levelSubs.process()

#    levelMult.process()
#
#    levelDiv.process()



#levelPSum.process()

# =============================================================================
# %% Algebra
# =============================================================================





# =============================================================================
# %% END
# =============================================================================

print(levelSum.n_page)

print(levelSubs.n_page)

print(levelMult.n_page)

print(levelDiv.n_page)

print(levelPSum.n_page)

print(levelOp.n_page)

print(levelFact.n_page)

print(levelequationSystems.n_page)


# =============================================================================
# %% END
# =============================================================================


