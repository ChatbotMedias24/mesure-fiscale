import streamlit as st
import openai
import streamlit as st
from dotenv import load_dotenv
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from streamlit_chat import message  # Importez la fonction message
import toml
import docx2txt
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
import docx2txt
from dotenv import load_dotenv
if 'previous_question' not in st.session_state:
    st.session_state.previous_question = []

# Chargement de l'API Key depuis les variables d'environnement
load_dotenv(st.secrets["OPENAI_API_KEY"])

# Configuration de l'historique de la conversation
if 'previous_questions' not in st.session_state:
    st.session_state.previous_questions = []

st.markdown(
    """
    <style>

        .user-message {
            text-align: left;
            background-color: #E8F0FF;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: 10px;
            margin-right: -40px;
            color:black;
        }

        .assistant-message {
            text-align: left;
            background-color: #F0F0F0;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: -10px;
            margin-right: 10px;
            color:black;
        }

        .message-container {
            display: flex;
            align-items: center;
        }

        .message-avatar {
            font-size: 25px;
            margin-right: 20px;
            flex-shrink: 0; /* Empêcher l'avatar de rétrécir */
            display: inline-block;
            vertical-align: middle;
        }

        .message-content {
            flex-grow: 1; /* Permettre au message de prendre tout l'espace disponible */
            display: inline-block; /* Ajout de cette propriété */
}
        .message-container.user {
            justify-content: flex-end; /* Aligner à gauche pour l'utilisateur */
        }

        .message-container.assistant {
            justify-content: flex-start; /* Aligner à droite pour l'assistant */
        }
        input[type="text"] {
            background-color: #E0E0E0;
        }

        /* Style for placeholder text with bold font */
        input::placeholder {
            color: #555555; /* Gris foncé */
            font-weight: bold; /* Mettre en gras */
        }

        /* Ajouter de l'espace en blanc sous le champ de saisie */
        .input-space {
            height: 20px;
            background-color: white;
        }
        .input-space {
        margin-top: 1px;
        margin-bottom: 1px;
    }
        @keyframes dot-blink {
            0% { content: ""; }
            33% { content: "."; }
            66% { content: ".."; }
            100% { content: "..."; }
        }
        .loading-message {
        margin-top: 1;
        padding-top: 1px;
        font-size: 20px;
        font-weight: bold;
        white-space: nowrap;
        animation: dot-blink 1.5s infinite step-start;
        
        }
    
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar contents
textcontainer = st.container()
with textcontainer:
    logo_path = "medi.png"
    logoo_path = "NOTEPRESENTATION.png"
    st.sidebar.image(logo_path,width=150)
   
    
st.sidebar.subheader("Suggestions:")
questions = [
    "Donnez-moi un résumé du rapport ",
    "Quelles sont les principales nouveautés fiscales introduites par la Loi de Finances 2025 ?",
    "Comment la réforme fiscale de 2025 impacte-t-elle les entreprises et les particuliers ?",      
    "Comment la réforme de l’IR réduit-elle la charge fiscale des personnes physiques ?",
    """Comment la réforme impacte-t-elle les opérations de restructuration des groupes de sociétés ?"""
]
# Initialisation de l'historique de la conversation dans `st.session_state`
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = StreamlitChatMessageHistory()

if 'previous_questions' not in st.session_state:
    st.session_state.previous_questions = []

# Ajouter une nouvelle question au début de la liste
def add_question(question):
    st.session_state.previous_questions.insert(0, question)
def main():
    text=r"""
    
                                         
                                      PREAMBULE


Dans le cadre des réformes structurelles menées pour assurer le financement des
politiques publiques et stimuler la croissance, le Gouvernement poursuit le processus de
mise en œuvre de la loi-cadre n° 69-19 portant réforme fiscale ayant tracé la feuille de
route de la politique fiscale de l’Etat, conformément aux recommandations des
troisièmes assises nationales de la fiscalité tenues les 03 et 04 mai 2019 à Skhirat.

En effet, après la réforme de l’impôt sur les sociétés (IS) en 2023 et de la taxe sur la
valeur ajoutée (TVA) en 2024, la loi de finances (LF) pour l’année budgétaire 2025 a
introduit la réforme de l’impôt sur le revenu (IR).

Cette réforme de l’IR vise essentiellement la baisse de la pression fiscale et l’amélioration
des revenus des salariés et des retraités, en application des recommandations de la loi-
cadre n° 69-19 précitée et des engagements du Gouvernement pris dans le cadre du
dialogue social.

Cette LF 2025 prévoit également d’autres mesures fiscales visant notamment :

      le renforcement des dispositifs fiscaux de lutte contre la fraude fiscale et
       l’intégration du secteur informel ;

      la clarification de certaines dispositions en matière de taxe sur la valeur ajoutée
       et des droits d’enregistrement ;

      la rationalisation et la simplification des règles d’assiette et de recouvrement de
       la parafiscalité, en intégrant dans le CGI les dispositions régissant la taxe spéciale
       sur le ciment.

La présente Note Circulaire a pour objet de présenter les mesures fiscales précitées
prévues par la LF 2025 par type d’impôt.




                                             5
I. MESURES SPECIFIQUES A L’IMPOT SUR LES SOCIETES
1- Augmentation des dotations aux amortissements déductibles fiscalement
   au titre des véhicules de transport de personnes
Avant l’entrée en vigueur de la LF 2025, l’article 10 (I-F-1°-b) du CGI prévoyait que le
taux d'amortissement du coût d'acquisition des véhicules de transport de personnes,
autres que ceux exclus expressément par cet article, ne peut être inférieur à 20% par
an et la valeur totale fiscalement déductible, répartie sur cinq (5) ans à parts égales,
ne pouvait être supérieure à trois cent mille (300 000) dirhams par véhicule, taxe sur
la valeur ajoutée (TVA) comprise.
Cet article prévoyait également que lorsque lesdits véhicules sont utilisés par les
entreprises dans le cadre d'un contrat de crédit-bail ou de location, la part de la
redevance ou du montant de la location supportée par l'utilisateur et correspondant à
l'amortissement au taux de 20% par an sur la partie du prix du véhicule excédant trois
cent mille (300 000) dirhams, n'est pas déductible pour la détermination du résultat
fiscal de l'utilisateur.
Compte tenu de l’augmentation des prix des véhicules, le seuil précité de déduction
des dotations aux amortissements des véhicules de transport de personnes a été
augmenté de trois cent mille (300 000) dirhams à quatre cent mille (400 000) dirhams
et ce, en vertu des dispositions de l’article 10 (I-F-1°-b) du CGI, telles que modifiées
par l’article 8 de la LF 2025.
Date d’effet :
L’article 8-IV-4 de la LF 2025 a prévu que les dispositions de l’article 10 (I-F-1°-b) du
CGI, telles que modifiées et complétées, sont applicables aux véhicules acquis
directement ou par voie de crédit-bail à compter du 1er janvier 2025.
NB : Concernant les véhicules utilisés par les entreprises dans le cadre d'un contrat de
location de longue durée ou avec option d’achat, le nouveau seuil de déduction de
(400 000) dirhams s’applique aux contrats conclus, permettant d’acquérir le droit
d’usage et/ou d’achat des véhicules concernés, à compter du 1er janvier 2025.
Exemples d’illustration :
Exemple n° 1 : Véhicule de transport de personnes acquis directement par
               une entreprise
Le 01/01/2025, la société « A » a acquis directement auprès d’un concessionnaire un
véhicule de transport de personnes.
      Prix d’acquisition :                                     500 000 DH TTC
      Annuité d’amortissement comptable : 500 000 x 20% = 100 000 DH
      Annuité d’amortissement déductible : 400 000 x 20%= 80 000 DH
    La réintégration fiscale à opérer annuellement est de :
               100 000 - 80 000 = 20 000 DH




                                           6
Exemple n° 2 : Véhicule de transport de personnes acquis par voie de
             contrat de crédit-bail (leasing)
Le 01/03/2025, la société « A » a acquis dans le cadre d’un contrat de crédit-bail un
véhicule de transport de personnes dans les conditions suivantes :
   Prix d’acquisition du véhicule : 720 000 DH TTC, soit 600 000 DH HT
   Durée du contrat : 48 mois
   Date de la première échéance : 31/03/2025
   Montant de la redevance mensuelle : 18 000 DH TTC
   Valeur résiduelle : 72 000 TTC
La société A a constaté la totalité des redevances de crédit-bail dans ses charges
d’exploitation, soit 180 000 DH (18 000 x 10 mois).
A la clôture de l’exercice, la société A doit réintégrer, d’une manière extracomptable,
la part non déductible de la redevance de crédit-bail.
Cette part non déductible est déterminée en comparant :
   1) le montant de l’amortissement supposé avoir été constaté chez la société de
      crédit-bail au taux de 20% sur la base du prix d’acquisition HT du véhicule, dès
      lors que la TVA est déductible chez la société de crédit-bail :
 (Prix d’acquisition HT X taux d’amortissement de 20%) X 10 mois d’amortissement
                                         /12)
                      (600 000 x 20%) x 10/12 = 100 000 DH
   2) avec la part de la redevance de crédit-bail correspondant à l'amortissement
      calculé sur la base du seuil de 400 000 DH TTC (333 333.33 DH HT).
                   (333 333.33 x 20%) x 10/12 = 55 555,55 DH
Ainsi, la part du montant de la redevance non déductible à réintégrer d’une manière
extra-comptable au résultat fiscal de l’exercice s'obtient comme suit :
                 (100 000 – 55 555,55) x 1,2 = 53 333,34 DH
NB : La part de la redevance à réintégrer s’obtient en ajoutant au montant HT de cette
part la TVA correspondante au taux de 20%, dès lors que cette TVA n’est pas
déductible chez la société utilisatrice (article 106 du CGI).
2- Révision du régime incitatif aux opérations de restructuration des
   groupes de sociétés
A- Rappel de l’évolution du régime incitatif
La LF 2017 a institué un régime d’incitation fiscale permettant le transfert des
immobilisations corporelles entre les sociétés soumises à l’IS, à l’exclusion des OPCI,
sans incidence sur leur résultat fiscal, si ce transfert est effectué entre les membres
d’un groupe de sociétés constitué à l’initiative d’une société mère qui détient d’une
manière continue, directement ou indirectement, 80% au moins du capital social
desdites sociétés, sous réserve du respect des conditions et obligations prévues par
les articles 20 bis et 161 bis-I du CGI.




                                          7
Le champ d’application de ce régime a été ensuite élargi aux immobilisations
incorporelles et financières par la LF 2020 et ce, dans le cadre de l’encouragement des
opérations de restructuration des groupes de sociétés, en vue de renforcer leur
compétitivité et de faciliter la réallocation de leurs moyens de production et de leurs
actifs.
B- Modifications introduites par la LF 2025
Dans le cadre de l’amélioration du régime d’incitation fiscale aux opérations de
restructuration des groupes de sociétés, tel que prôné par la loi cadre n° 69-19 portant
réforme fiscale, la LF 2025 a introduit plusieurs modifications au niveau des articles 20
bis et 161 bis-I du CGI.
 a) Réduction du seuil de participation dans les sociétés détenues par la
    société mère du groupe
En vue d’encourager les opérations de restructuration intragroupe, le seuil de
participation détenue, d’une manière continue directement ou indirectement, par la
société mère dans le capital social des sociétés du groupe a été réduit de 80% à deux
tiers (2/3), pour le bénéfice du régime d’incitation fiscale prévu par l’article 161 bis-I
du CGI.
NB : Les groupes de sociétés déjà déclarés à l’administration fiscale continuent à
bénéficier dudit régime d’incitation fiscale aux opérations de restructuration, en cas de
modification de leur composition pour intégrer de nouvelles sociétés dont la société
mère détient au moins les deux tiers (2/3) du capital à partir du 1er janvier 2025 ou en
cas de réduction, à partir de la même date, de la participation de la société mère dans
les sociétés déjà membres à deux tiers (2/3), sous réserve du respect des conditions
et des obligations déclaratives prévues par les articles 20 bis et 161 bis-I du CGI, tel
que modifié et complété.
 b) Modification de        la   définition       de   la   notion   de   transfert    des
    immobilisations
Avant l’entrée en vigueur de la LF 2025, le transfert des immobilisations visé à l’article
161 bis-I du CGI s’entendait de toute opération se traduisant par un transfert de
propriété des immobilisations corporelles, incorporelles et financières inscrites à l’actif
immobilisé entre les sociétés membres du même groupe, y compris les opérations
générant un flux financier, telle que la vente en contrepartie d’une rémunération.
Dans le cadre de la rationalisation du régime incitatif prévu par l’article 161 bis-I du
CGI, la LF 2025 a modifié la définition de la notion de transfert pour la limiter aux
opérations se traduisant par un transfert de propriété desdites immobilisations entre
les sociétés membres du même groupe, en contrepartie de l’octroi de titres de
participation dans le capital social de la société ayant bénéficié du transfert de ces
immobilisations.
Suite à cette modification, une nouvelle condition a été prévue pour l’éligibilité au
régime incitatif prévu à l’article 161 bis-I du CGI. Ainsi, il a été prévu que les titres
reçus par les sociétés concernées en contrepartie du transfert des immobilisations
précitées ne doivent être ni cédés, ni retirés ou apportés à une autre société
n’appartenant pas au groupe.




                                             8
 c) Possibilité d’opter pour la méthode d’évaluation des immobilisations
    transférées à leur valeur réelle ou à leur valeur nette comptable
Avant l’entrée en vigueur de la LF 2025, les immobilisations transférées dans le cadre
du régime d’incitation fiscale aux opérations de restructuration des groupes de sociétés
devaient être évaluées à leur valeur réelle au jour du transfert.
En vue d’améliorer ce régime, l’article 8 de la LF 2025 a complété les dispositions de
l’article 161 bis-I du CGI, afin d’instituer la possibilité d’opter soit pour la méthode
d’évaluation des immobilisations transférées à leur valeur réelle à la date du transfert,
soit pour la méthode d’évaluation desdites immobilisations à leur valeur nette
comptable (VNC).
   1) Méthode d’évaluation des immobilisations transférées à leur valeur
      réelle à la date du transfert
En cas d’option pour l’évaluation des immobilisations transférées à leur valeur réelle à
la date du transfert, les sociétés ayant transféré ces immobilisations bénéficient d’un
sursis de paiement de l’IS correspondant à la plus-value nette résultant de ce transfert.
A ce titre, il est rappelé que les sociétés ayant bénéficié du transfert des
immobilisations ne peuvent déduire de leur résultat fiscal les dotations aux
amortissements et aux provisions de ces immobilisations que dans la limite des
dotations aux amortissements et aux provisions calculées sur la base de leur valeur
d’origine figurant dans l’actif de la société du groupe ayant opéré la première opération
de transfert.
Toutefois, en cas de cession ultérieure des immobilisations transférées à leur valeur
réelle, les amortissements réintégrés durant la période de la détention desdites
immobilisations chez la société ayant bénéficié du transfert sont déduits extra-
comptablement, vu que la plus-value nette imposable chez cette société est
déterminée, dans ce cas, compte tenu des amortissements comptables pratiqués,
sachant que la société ayant opéré le transfert initial doit régulariser sa situation fiscale
en payant l’IS ayant fait l’objet de sursis de paiement.
   2) Méthode d’évaluation des immobilisations transférées à leur valeur
      nette comptable à la date du transfert
En cas d’option pour l’évaluation des immobilisations transférées à leur valeur nette
comptable (VNC), ces immobilisations sont inscrites dans le bilan des sociétés
bénéficiaires du transfert à leur valeur, avant l’opération de transfert, figurant au
dernier bilan clos des sociétés ayant procédé au transfert.
Ainsi, la société ayant bénéficié du transfert des immobilisations précitées reprend à
son actif la valeur d’origine des immobilisations transférées et les amortissements et
provisions y afférents, à la date de transfert, le cas échéant, tels qu’ils étaient constatés
par la société ayant effectué le transfert.
De ce fait, la société ayant bénéficié du transfert continue à calculer les dotations aux
amortissements et provisions sur la base de la valeur d’origine qu’avaient lesdites
immobilisations dans l’actif de la société ayant opéré le transfert.




                                             9
 d) Institution de la règle du sursis de paiement de l’IS sur la plus-value
    nette réalisée
Avant l’entrée en vigueur de la LF 2025, les dispositions de l’article 161 bis-I du CGI
prévoyaient que les immobilisations corporelles, incorporelles et financières
transférées devaient être évaluées à leur valeur réelle au jour du transfert et que la
plus-value résultant du transfert desdites immobilisations bénéficie du sursis
d’imposition et elle n’est donc pas prise en considération pour la détermination du
résultat fiscal des sociétés ayant opéré le transfert.
En vue de rationaliser le mode de régularisation de l’imposition des plus-values
réalisées lors du transfert des immobilisations à la valeur réelle, la LF 2025 a modifié
les dispositions de l’article 161 bis-I précité pour instituer la règle du sursis de paiement
de l’IS correspondant à la plus-value nette résultant de ce transfert, au lieu du sursis
d’imposition des plus-values et ce, à l’instar de ce qui est prévu dans les autres régimes
incitatifs de restructuration des entreprises.
L’IS objet du sursis de paiement est calculé sur la base de la plus-value nette résultant
de l’opération de transfert au taux en vigueur lors de la réalisation de cette
opération.
Il est rappelé que sur le plan comptable, l’IS ayant fait l’objet de sursis du paiement
doit être constaté dans les comptes de la société apporteuse.
En effet, le CGNC prévoit que la charge probable d'impôt rattachable à l'exercice mais
différée dans le temps et dont la prise en compte définitive dépend d'éléments futurs,
doit être comptabilisée dans le compte n° 1551 « Provisions pour impôts » sachant
que cette provision de l’IS n’est pas déductible fiscalement.
A titre de rappel, en cas de non-respect des conditions prévues par l’article 161 bis-I
du CGI, la situation de toutes les sociétés du groupe concernées par les opérations de
transfert d’une immobilisation est régularisée, selon les règles de droit commun,
comme s’il s’agissait d’opérations de cessions et ce, au titre de l’exercice au cours
duquel la défaillance est intervenue.
Ainsi, les sociétés concernées doivent verser spontanément l’IS ayant fait l’objet de
sursis du paiement, par procédé électronique, selon un modèle établi par
l’administration à cet effet, dans les trois mois suivant la date de clôture de l’exercice
de défaillance.
Il est à signaler qu’en cas de cession partielle des titres acquis en contrepartie du
transfert des immobilisations, le versement du montant de l’IS, ayant fait l’objet de
sursis de paiement, est effectué au prorata des titres cédés.
 e) Obligations des sociétés du groupe concernées par le transfert des
    immobilisations
Dans le cadre de l’harmonisation, la LF 2025 a complété les dispositions de l’article 20
bis du CGI, pour préciser les renseignements à servir dans l’état produit par les sociétés
ayant transféré les immobilisations et celles ayant bénéficié du transfert desdites
immobilisations, dans les trois (3) mois qui suivent la date de clôture de l’exercice de
transfert, comme suit :
  - la valeur d’origine figurant à l’actif de la société du groupe ayant opéré la
    première opération de transfert ;


                                             10
  - la valeur choisie pour l’évaluation des immobilisations transférées ;
  - la valeur nette comptable desdites immobilisations ;
  - la valeur réelle des immobilisations au jour du transfert ;
  - l’impôt sur les sociétés correspondant à la plus-value nette résultant de
    l’opération de transfert ayant fait l’objet de sursis de paiement ;
  - la valeur des titres acquis en contrepartie dudit transfert.
Il a été également prévu qu’en cas de cession totale ou partielle des titres acquis en
contrepartie du transfert desdites immobilisations, le service local des impôts doit être
avisé par la société concernée.
NB : Eu égard au nouveau seuil de participation de la société mère dans le capital
social des sociétés membres du groupe de sociétés, la composition de ce groupe peut
être modifiée, sous réserve du respect des obligations prévues par les dispositions de
l’article 20 bis du CGI.
Date d’effet :
Conformément aux dispositions de l’article 8-IV-5 de la LF 2025, les nouvelles
dispositions des articles 20 bis et 161 bis-I du CGI, sont applicables aux opérations de
transfert des immobilisations réalisées à compter du 1er janvier 2025.
Exemples d’illustration :
La société « A » fait partie d’un groupe de sociétés composé d’une société mère (M)
et de trois sociétés filiales (A, B et C), éligible au régime d’incitation fiscale prévu à
l’article 161 bis-I du CGI.
En mars 2022, la société mère a déclaré le groupe à l’administration fiscale.
Le 1er janvier 2025, la société A procède à l’apport d’un bien immeuble à la société B.
Ce bien a été acquis le 1er janvier 2016 à une valeur d’origine (VO) de 11 000 000 DH
et il est constitué des éléments suivants :
       -     un terrain acquis au prix de : 4 000 000 DH
       -     des constructions au prix de : 7 000 000 DH
En contrepartie de cet apport, la société « A » a reçu des titres de la société B.
Les constructions apportées sont amorties au taux de 4%.
  Cas d’évaluation des immobilisations apportées à leur valeur réelle (VR)
La société « A », qui exerce uniquement une activité de négoce et qui réalise la totalité
de son chiffre d’affaires localement, a opté pour la méthode d’évaluation des
immobilisations apportées à leur valeur réelle (VR) à la date d’apport.
La déclaration du résultat fiscal (RF) de l’exercice 2025, souscrite avant le 1 er avril
2026, fait ressortir les éléments suivants :
          Bénéfice hors plus-value (PV) nette d’apport : 90 000 000 DH
          PV nette d’apport :                           13 520 000 DH
Cette plus-value est calculée comme suit :




                                           11
         Libellé                               VO           VNC             VR         Plus-value
          Terrain                     4 000 000           4 000 000     10 000 000      6 000 000
     Constructions                    7 000 000           4 480 0001    12 000 000      7 520 000
           Total                    11 000 000            8 480 000     22 000 000     13 520 000

          Bénéfice net fiscal de l’exercice 2025 :
                                                    90 000 000 + 13 520 000 = 103 520 000 DH
          IS objet de sursis du paiement : 13 520 000 x 34% = 4 596 800 DH
Vu que le bénéfice net fiscal de l’exercice 2025 est supérieur à 100 000 000 DH, le
montant de l’IS objet de sursis du paiement est calculé au taux en vigueur au titre de
cet exercice, soit 34%.
          IS dû au titre de l’exercice 2025 : 90 000 000 x 34% = 30 600 000 DH
          IS théorique devant servir de base de calcul des acomptes à verser au titre de
           l’exercice 2026 :                 90 000 000 x 20% = 18 000 000 DH
N.B : Les acomptes provisionnels à verser au titre de l’exercice 2026 sont déterminés
au taux de 20%, conformément aux dispositions des articles 19-I-B et 247-XXXVII-A
du CGI tels que modifié par la LF 2024 qui prévoient que lorsqu’une société réalise au
titre d’un exercice un bénéfice net égal ou supérieur à cent millions (100 000 000) de
dirhams suite à la réalisation des produits non courants de cession d’immobilisations
visés à l’article 9-I-C-1° du CGI, le taux majoré progressivement pour atteindre le taux
cible de 35% s’applique uniquement au titre de cet exercice (soit 34% pour l’exercice
2025 dans le cas d’espèce).
     Cas d’évaluation des immobilisations apportées à leur valeur nette
      comptable (VNC)
Dans ce cas, l’opération de transfert est réalisée sans incidence sur le résultat fiscal de
la société « A » ayant procédé à l’apport, dès lors qu’aucune plus-value ne sera
constatée et elle doit produire l’état prévu à l’article 20 bis du CGI.
La société « B » doit inscrire les immobilisations transférées dans son actif immobilisé
à leur valeur, avant l’opération de transfert, figurant au dernier bilan clos de la société
« A » ayant procédé au transfert.
A ce titre, la société « B » doit reprendre à son bilan les écritures comptables de la
société « A » telles qu’elles figuraient dans le bilan de cette dernière notamment, la
valeur d’origine des immobilisations transférées ainsi que les amortissements y
afférents constatés à la date du transfert et doit continuer à calculer les dotations aux
amortissements sur la base de la valeur d’origine précitée.




1
7 000 000 – (7 000 000 x 4% x 9) = 4 480 000




                                                              12
II. MESURES SPECIFIQUES A L’IMPOT SUR LE REVENU
 1- Réduction de la charge fiscale des personnes physiques
 La réforme de l’IR s’inscrit dans le cadre de la continuité de la mise en œuvre de la loi-
 cadre n° 69-19 portant réforme fiscale visant, notamment, la baisse de la pression
 fiscale sur les contribuables au fur et à mesure de l’élargissement de l’assiette.
 Cette réforme s’inscrit également dans le cadre de l’exécution de l’engagement du
 Gouvernement prévu par l’accord d’avril 2024 relatif au dialogue social, afin d’améliorer
 les revenus des fonctionnaires et des salariés, à travers la réduction de leur charge
 fiscale en matière de l’IR.
 Pour ce faire, la LF 2025 a introduit les mesures suivantes :
   A- Réaménagement du barème progressif de l’IR
 Le réaménagement du barème progressif de l’IR prévu à l’article 73-I du CGI se
 présente comme suit :
     - le relèvement de la première tranche du barème relative au revenu net exonéré
       de 30 000 à 40 000 dirhams ;
     - la révision des autres tranches du barème, afin de les élargir et de réduire leur
       taux d’imposition ;
     - la réduction du taux marginal du barème précité de 38% à 37%.
 Ces modifications se présentent comme suit :

              Avant la LF 2025                                 Après la LF 2025

     Tranches de                 Sommes à            Tranches de                  Sommes à
                        Taux                                            Taux
       revenu                     déduire              revenu                      déduire
 0 à 30 000              0%           0           0 à 40 000             0%           0
 30 001 à 50 000         10%        3 000         40 001 à 60 000       10%         4 000
 50 001 à 60 000         20%        8 000         60 001 à 80 000       20%        10 000
 60 001 à 80 000         30%        14 000        80 001 à 100 000      30%        18 000
 80 001 à 180 000        34%        17 200        100 001 à 180 000     34%        22 000
 Au-delà de 180 000      38%        24 400        Au-delà de 180 000    37%        27 400

 Date d’effet :
 Conformément aux dispositions de l’article 8-IV (10 et 12) de la LF 2025, les
 dispositions de l’article 73-I du CGI, telles que modifiées, sont applicables :
     aux revenus, autres que fonciers, acquis à compter du 1er janvier 2025 ;
     et aux revenus fonciers encaissés à compter du 1er janvier 2025.
 NB : Il est rappelé que la note circulaire n° 717 relative au CGI a défini les revenus
 acquis comme étant ceux sur lesquels le contribuable a un droit incontestable.
 Ainsi, si un salarié perçoit des rappels de salaires, ces derniers constituent des
 compléments aux paiements déjà effectués au cours des périodes antérieures. De ce
 fait, ils sont à rattacher auxdites périodes.


                                             13
De même, les primes et rappels de salaires acquis au titre de l’année 2024 et versés
en 2025 sont soumis, en matière d’IR, aux taux du barème en vigueur au 31 décembre
2024.
Par contre, les primes et gratifications non acquises au titre de l’année 2024, du fait
que leur fait générateur intervient au cours de l’année 2025, sont soumises aux taux
du barème de l’IR en vigueur au 1er janvier 2025. C’est le cas des primes et
gratifications déterminées en fonction du résultat de l’entreprise (primes de bilan, de
productivité, d’intéressement, etc.) et qui sont attribuées aux salariés au cours de
l’année qui suit celle de la réalisation dudit résultat, elles ne sont acquises qu’après
réalisation dudit résultat.
De ce fait, les primes et gratifications déterminées en fonction du résultat de l’année
2024 et versées au cours de l’année 2025 sont à considérer comme des rémunérations
de l’année 2025 soumises, en matière d’IR, aux taux du barème en vigueur à compter
du 1er janvier 2025.
  B- Augmentation du seuil d’application de la retenue à la source au titre
     des revenus fonciers
Dans le cadre de l’harmonisation avec le réaménagement du barème progressif des
taux de l’IR, notamment le relèvement de la première tranche du barème relative au
revenu net exonéré de 30 000 à 40 000 dirhams, la LF 2025 a relevé le seuil
d’application de la retenue à la source prévue à l’article 160 bis du CGI sur les revenus
fonciers, aux taux non libératoires de 10% ou 15%, de 30 000 à 40 000 dirhams.
Ainsi, les personnes morales de droit public ou privé ainsi que les personnes physiques
dont les revenus professionnels sont déterminés selon le régime du résultat net réel
ou celui du résultat net simplifié, sont dispensées de l’obligation de la retenue à la
source à opérer aux taux non libératoires de 10% ou 15%, lorsque le montant des
revenus fonciers annuels bruts imposables versé à un propriétaire ne dépasse pas
40 000 dirhams.
Il convient de préciser que cette dispense d’application de la retenue à la source ne
s’applique pas aux revenus fonciers versés aux personnes ayant opté pour l’imposition
desdits revenus selon le taux libératoire de 20%.
Par ailleurs, il est rappelé que les contribuables disposant de revenus fonciers ne
dépassant pas 40 000 dirhams et/ou d’autres revenus soumis au barème, sont tenus
de souscrire leur déclaration annuelle de revenu global au titre de l’ensemble de ces
revenus, à l’exception des revenus fonciers ayant fait l’objet de la retenue à la source
au taux libératoire de 20% suite à leur option.
Date d’effet :
Conformément aux dispositions de l’article 8-IV-10 de la LF 2025, les dispositions de
l’article 160 bis du CGI, telles que modifiées et complétées, sont applicables aux
revenus fonciers encaissés à compter du 1er janvier 2025.
  C- Augmentation du montant annuel de la réduction de l’IR au titre des
     charges de famille
La LF 2025 a modifié les dispositions de l’article 74-I du CGI, afin d’augmenter le
montant annuel de la réduction de l’IR au titre des charges de famille de 360 à 500
dirhams par personne à charge.


                                           14
De ce fait, le plafond annuel de cette réduction a été également porté de 2160 à 3000
dirhams, en maintenant ainsi le bénéfice de cette réduction pour six (6) personnes à
charge.
Il est rappelé que sont à la charge du contribuable :
      son épouse ;
      ses propres enfants ainsi que les enfants légalement recueillis par lui à son
       propre foyer à condition :
         -   qu'ils ne disposent pas, par enfant, d'un revenu global annuel supérieur à
             la tranche exonérée du barème de calcul de l’IR, soit 40 000 dirhams ;
         -   que leur âge n'excède pas 27 ans. Cette condition d'âge n'est, toutefois,
             pas applicable aux enfants atteints d'une infirmité les mettant dans
             l'impossibilité de subvenir à leurs besoins.
Il est rappelé également que la femme contribuable bénéficie des réductions pour
charge de famille au titre de son époux et de ses enfants, lorsqu'ils sont légalement à
sa charge dans les mêmes conditions précitées.
Date d’effet :
Conformément aux dispositions de l’article 8-IV (10 et 12) de la LF 2025, les
dispositions de l’article 74-I du CGI, telles que modifiées, sont applicables :
    aux revenus autres que fonciers acquis à compter du 1er janvier 2025 ;
    et aux revenus fonciers encaissés à compter du 1er janvier 2025.
  D- Relèvement du montant admis en exonération des bons représentatifs
    des frais de nourriture ou d’alimentation délivrés par les employeurs à
    leurs salariés
Au regard des dispositions de l’article 57-13° du CGI en vigueur avant le 1er janvier
2025, les bons représentatifs des frais de nourriture ou d’alimentation délivrés par les
employeurs à leurs salariés, afin de leur permettre de régler tout ou partie des prix
des repas ou des produits alimentaires étaient exonérés de l’IR, dans la limite de 30
dirhams par salarié et par jour de travail.
Dans le cadre du soutien aux salariés, la LF 2025 a modifié les dispositions de l’article
57-13° précité pour relever, à compter du 1er janvier 2025, le montant exonéré des
bons précités de 30 à 40 dirhams, avec possibilité du paiement desdits bons par
procédé électronique.
Il convient de rappeler que les dispositions de l’article 57-13° précité prévoient que le
montant de ces frais ne peut en aucun cas être supérieur à 20% du salaire brut
imposable et que cette exonération ne peut être cumulée avec les indemnités
alimentaires accordées aux salariés travaillant dans des chantiers éloignés de leur lieu
de résidence.
  E- Exonération de l’IR des pensions de retraite et des rentes viagères
     versées dans le cadre des régimes de retraite de base
Avant le 1er janvier 2025, les pensions de retraite et les rentes viagères étaient
soumises à l’IR aux taux du barème progressif visé à l’article 73-I du CGI, après
application de l’abattement forfaitaire prévu à l’article 60-I dudit code, fixé comme
suit :

                                           15
     - 70% sur le montant brut desdites pensions et rentes viagères qui ne dépasse
       pas annuellement 168 000 DH ;
     - 40% pour le surplus.
Dans le cadre de la réforme de l’IR et afin de soutenir le pouvoir d’achat des retraités,
la LF 2025 a institué l’exonération de l’IR pour les pensions de retraite et rentes
viagères versées dans le cadre des régimes de retraite de base, selon la démarche
progressive suivante :
       l’application, à titre transitoire, d’une réduction de 50% de l’IR au titre des
        pensions de retraite et rentes viagères, acquises dans le cadre des régimes
        de retraite de base, au titre de l’année 2025 ;
       l’exonération totale de l’IR desdites pensions de retraite et rentes viagères
        acquises, dans le cadre des régimes de retraite de base, à compter du 1er
        janvier 2026.
       a) Réduction de 50% de l’IR pour les pensions de retraite et des
          rentes viagères acquises dans le cadre des régimes de retraite de
          base au titre de l’année 2025
L’article 8-IV-8 de la LF 2025 a prévu qu’à titre transitoire et nonobstant toutes
dispositions contraires, les titulaires des pensions de retraite et des rentes viagères
acquises dans le cadre des régimes de retraite de base visés à l’article 59-II-A du CGI,
à l’exclusion de celles acquises dans le cadre des régimes de retraite complémentaire,
bénéficient d’une réduction de 50% du montant de l’IR dû au titre desdites pensions
de retraite et rentes viagères acquises au titre de l’année 2025.
       b) Exonération totale de l’IR des pensions de retraite et des rentes
          viagères acquises dans le cadre des régimes de retraite de base à
          compter du 1er janvier 2026
L’article 57-27° du CGI, tel que complété par l’article 8 de la LF 2025, prévoit que sont
exonérées de l’IR, les pensions de retraite et les rentes viagères versées dans le cadre
des régimes de retraite de base visés à l’article 59-II-A dudit code, à l’exclusion de
celles versées dans le cadre des régimes de retraite complémentaire.
Cette exonération s’applique, notamment, aux retraites de base versées dans le cadre :
   - du régime des pensions civiles institué par la loi n° 11 - 71 du 12 kaada 1391 (30
     décembre 1971) ;
   - du régime des pensions militaires institué par la loi n° 13-71 du 12 kaada 1391
     (30 décembre 1971) ;
   - du régime collectif d'allocation de retraite (RCAR) institué par le dahir portant loi
     n° 1-77-216 du 20 chaoual 1397 (4 octobre 1977) ;
   - du régime de sécurité sociale (CNSS) régi par le dahir portant loi n° 1-72-184 du
     15 joumada II 1392 (27 juillet 1972) ;
   - des régimes de retraite prévus par les statuts des organismes marocains de
     retraite constitués et fonctionnant conformément à la législation et à la
     réglementation en vigueur en la matière.




                                           16
Ainsi, l’exonération précitée ne concerne pas les pensions de retraite et les rentes
viagères versées dans le cadre des régimes de retraite complémentaire qui demeurent
soumises à l’IR dans les conditions de droit commun, à savoir l’imposition aux taux du
barème progressif visé à l’article 73-I du CGI après application, le cas échéant, de
l’abattement forfaitaire prévu à l’article 60-I dudit code. Il s’agit notamment des
pensions de retraite et des rentes viagères versées par :
   - la Caisse Interprofessionnelle Marocaine de Retraite (CIMR) ;
   - le régime complémentaire du RCAR ;
   - le régime de retraite complémentaire CMR-ATTAKMILI ;
   - et les autres instruments d’épargne retraite facultatifs qui donnent droit à une
     pension complémentaire.
Quant aux pensions de retraite de source étrangère, elles demeurent soumises à l’IR
aux taux du barème progressif visé à l’article 73-I du CGI, après application de
l’abattement forfaitaire prévu à l’article 60-I précité, avec possibilité de bénéficier de
la réduction de 80% du montant de l’impôt dû au titre de ces pensions et
correspondant aux sommes transférées à titre définitif en dirhams non convertibles,
prévue à l’article 76 du CGI.
La LF 2025 a également modifié et complété les dispositions de l’article 86 (5° et 7°)
du CGI pour prévoir la dispense de l’obligation de dépôt de la déclaration annuelle du
revenu global pour :
     les contribuables disposant uniquement de pensions de retraite dans le cadre
      des régimes de retraite complémentaire, payées par plusieurs débirentiers
      domiciliés ou établis au Maroc et tenus d’opérer la retenue à la source telle que
      prévue à l’article 156-I du CGI, dont le total cumulé du montant net imposable
      au titre desdites pensions n’excède pas le seuil exonéré de 40 000 DH prévu à
      l’article 73-I dudit code ;
     les contribuables disposant uniquement de pensions de retraite et rentes
      viagères exonérées de l’IR visées à l’article 57-27° précité.
NB : Les pensions de retraite et rentes viagères exonérées de l’IR en vertu de l’article
57-27° du CGI ne sont pas prises en considération dans la base imposable du
contribuable disposant d’autres revenus imposables.
Date d’effet
L’article 8-IV-8 de la LF 2025 prévoit que l’exonération totale de l’IR et la dispense de
la déclaration prévues par les dispositions des articles 57-27° et 86 (5° et 7°) du CGI,
telles que modifiées et complétées, s’appliquent aux pensions de retraite et rentes
viagères acquises, dans le cadre des régimes de retraite de base, à compter du 1er
janvier 2026.
Exemples d’illustration :
Exemple n° 1 : Cas d’un contribuable disposant d’une pension de retraite au
titre de l’année 2025
Un contribuable marié bénéficie au titre de l’année 2025 d’une pension de retraite
annuelle de source marocaine versée dans le cadre d’un régime de retraite de base,
d’un montant brut de 240 000 DH :


                                           17
Calcul de la base imposable :
    Montant brut de la pension : ………………………………………….………240 000 DH
    Montant de l’abattement : (168 000 x 70%) + (72 000 x 40%) : 146 400 DH
    Retenues au titre de l’AMO : ………………………………….……….…………4 800 DH
    Montant net imposable : 240 000 - 146 400- 4 800 …………...…... 88 800 DH
Calcul de l’impôt dû :
    Montant de l’IR calculé : (88 800 x 30%) – 18 000 :……..……….... 8 640 DH
    Réduction de 50% de l’impôt dû : (8 640 X 50%) :…………… 4 320 DH
    Réduction pour charge de famille (marié) : ............................500 DH
              Soit un impôt dû de : 8 640 – 4 320 – 500 = 3 820 DH
Exemple n° 2 : Cas d’un contribuable disposant au titre de l’année 2026 des
pensions de retraite et d’un revenu foncier
Un contribuable marié bénéficie au titre de l’année 2026 :
   -   d’une pension de retraite de source marocaine versée dans le cadre d’un
       régime de retraite de base, d’un montant annuel brut de 120 000 DH,
   -   d’une pension de retraite de source marocaine versée dans le cadre des régimes
       de retraite complémentaire, servie sous forme d’une rente viagère d’un
       montant annuel brut de 80 000 DH,
   -   et d’un revenu foncier annuel brut imposable de 180 000 DH provenant de la
       location de trois appartements à usage d’habitation à des particuliers.
Dans ce cas, ledit contribuable est tenu de souscrire sa déclaration annuelle du revenu
global avant le 1er mars 2027 et de verser spontanément, dans ce même délai, le
montant de l’IR correspondant à sa retraite complémentaire servie sous forme d’une
rente viagère et son revenu foncier.
Quant à la pension de retraite versée dans le cadre d’un régime de retraite de base,
elle est exonérée de l’IR en vertu de l’article 57-27° du CGI et n’est pas prise en
considération dans la base imposable du revenu global imposable dudit contribuable.
Ainsi, le montant de l’IR correspondant aux revenus précités est liquidé comme suit :
Détermination de la base imposable :
 Montant du revenu foncier annuel brut………………..……………...…..180 000 DH
      Abattement au titre des revenus fonciers : 180 000 x 40% ……….. 72 000 DH
      Montant du revenu foncier net imposable : 180 000 – 72 000 ….108 000 DH
 Montant brut de la rente viagère versée dans le cadre des régimes de retraite
  complémentaire………………………………………..……………….……….……… 80 000 DH
      Abattement au titre de la rente viagère : 80 000 x 70% ………….... 56 000 DH
      Montant net imposable de la rente viagère : 80 000 – 56 000 …….24 000 DH
 Revenu global net imposable : 108 000 + 24 000 …………..…….132 000 DH




                                          18
Calcul de l’impôt dû :
    Montant de l’IR calculé : (132 000 x 34%) – 22 000 :……..…….. 22 880 DH
    Réduction pour charge de famille (marié) : ..................................500 DH
                  Soit un impôt dû de : 22 880 – 500 = 22 380 DH
2- Révision des conditions d’exonération de l’indemnité de stage pour la
   promotion de l’emploi
Avant le 1er janvier 2025, les dispositions de l’article 57-16° du CGI exonéraient de l’IR
l’indemnité de stage mensuelle brute plafonnée à 6 000 dirhams, versée au stagiaire
lauréat de l’enseignement supérieur ou de la formation professionnelle ou titulaire d’un
baccalauréat, par les entreprises du secteur privé pour une période de 24 mois, sous
réserve du respect des conditions prévues par ledit article.
Dans le cadre de la mise en œuvre de la feuille de route pour la promotion de l’emploi
et afin de pallier la problématique de recrudescence des chômeurs non qualifiés, la LF
2025 a modifié les dispositions de l’article 57-16° précité pour introduire les mesures
suivantes :
    - l’élargissement du bénéfice de l’exonération précitée au titre de l’indemnité de
      stage mensuelle brute plafonnée à 6 000 dirhams à tous les stagiaires, y
      compris les non-diplômés ;
    - la réduction de la période de stage éligible à cette exonération de vingt-quatre
      (24) mois à douze (12) mois ;
    - la continuité du bénéfice du stagiaire de l’exonération au titre de l’indemnité de
      stage dans la limite de douze (12) mois, en cas de changement de l’employeur ;
    - l’application de l’exonération de l’IR pour une période de vingt-quatre (24) mois,
      en cas de recrutement du stagiaire dans le cadre d’un contrat de travail à durée
      indéterminée, pour le salaire mensuel brut plafonné à dix mille (10 000)
      dirhams.
Ainsi, l’indemnité de stage mensuelle brute plafonnée à six mille (6 000) dirhams
versée au stagiaire par les entreprises du secteur privé bénéficie de l’exonération de
l’IR, pour une période de douze (12) mois.
A ce titre, il convient de rappeler qu’en vertu des dispositions de l’article 57-16°
précitée, lorsque le montant de l’indemnité de stage versée est supérieur au plafond
de six mille (6 000) dirhams, il perd le bénéfice de l’exonération et devient imposable
dans son intégralité à l’IR, dans les conditions de droit commun.
L’exonération précitée est accordée dans les conditions suivantes :
    - les stagiaires doivent être inscrits à l’ANAPEC ;
    - l’application de cette exonération une seule fois pour le même stagiaire.
      Toutefois, en cas de changement d’employeur, le stagiaire peut continuer à
      bénéficier de l’exonération dans la limite des douze (12) mois précités ;
    - l’employeur doit s’engager à procéder au recrutement définitif d’au moins 60%
      desdits stagiaires.




                                             19
En cas de respect des conditions précitées et de recrutement du stagiaire dans le cadre
d’un contrat de travail à durée indéterminée, le salaire mensuel brut plafonné à dix
mille (10 000) dirhams versé à ce dernier, bénéficie également de l’exonération de l’IR
pour une période de vingt-quatre (24) mois.
Il est à rappeler que le salaire mensuel brut correspond au montant total des
rémunérations brutes d’un salarié, avant application des exonérations et déductions
prévues aux articles 57 et 59 du CGI.
Il est rappelé que les modalités de détermination du taux de 60% de recrutement des
bénéficiaires de contrats d’insertion ont été fixées par le décret n° 2-15-906 du 07
mars 2016 pris pour l’application du dahir n° 1.93.16 fixant les mesures
d’encouragement aux entreprises organisant des stages au profit des titulaires de
certains diplômes en vue de leur formation-insertion tel que modifié et complété.
En cas de non-respect de la condition de recrutement définitif d’au moins 60% des
stagiaires, l’IR est régularisé dans les conditions de droit commun.
Date d’effet :
Les dispositions de l’article 57-16° du CGI, telles que modifiées et complétées par le
paragraphe I de l’article 8 de la LF 2025, sont applicables aux contrats conclus à
compter du 1er janvier 2025.
Ainsi, les contrats de stage conclus avant le 1er janvier 2025 demeurent régis par les
dispositions de l’article 57-16° précité en vigueur avant cette date.
3- Amélioration du régime de l’IR au titre des revenus fonciers
Avant le 1er janvier 2025, les titulaires de revenus fonciers soumis à la retenue à la
source (RAS) étaient tenus de souscrire une déclaration au titre de leur revenu global
en fin d’année après imputation, le cas échéant, de la RAS opérée au cours de l’année
concernée au taux non libératoire de 10% ou 15% prévus par l’article 73-II (B-5° et
C-4°) du CGI.
Afin d’assurer l’équité fiscale et de simplifier ce mode d’imposition, notamment pour
les salariés et les retraités, la LF 2025 a modifié et complété les dispositions des articles
64-IV, 73 (II-F-12°), 86-6° et 160 bis du CGI, pour octroyer aux contribuables
concernés la possibilité d’opter pour l’imposition de ces revenus, pour leur montant
brut, au taux libératoire de 20% prévu à l’article 73-II-F-12° dudit code.
   A. Contribuables concernés
L’article 64 du CGI a été complété par un nouveau paragraphe IV prévoyant que les
contribuables disposant de revenus fonciers soumis à la RAS peuvent opter pour
l’imposition desdits revenus selon le taux libératoire de 20%, sur la base du montant
brut imposable des revenus fonciers prévu au I dudit article.
A ce titre, il est rappelé que les revenus fonciers soumis à la RAS, en vertu des
dispositions de l’article 160 bis du CGI, sont ceux versés par les personnes morales de
droit public ou privé ainsi que les personnes physiques dont les revenus professionnels
sont déterminés selon le régime du résultat net réel ou celui du résultat net simplifié,
à des personnes physiques.




                                             20
   B. Modalités d’option à l’imposition selon le taux libératoire
Pour opter pour l’imposition selon le taux libératoire, une demande doit être souscrite
par les contribuables concernés, au titre de leurs revenus fonciers soumis à la retenue
à la source, par procédé électronique, auprès de l’administration fiscale contre
récépissé, selon un modèle établi à cet effet.
Les contribuables concernés doivent remettre une copie du récépissé précité aux
locataires chargés d’opérer la RAS, au moins 30 jours avant la date de l’échéance du
versement du loyer du mois qui suit celui de dépôt de la demande d’option.
Ladite option prend effet à compter du mois qui suit celui de la remise de la copie du
récépissé précité aux personnes chargées d’opérer la retenue à la source.
A ce titre, il convient de préciser que cette option concerne l’ensemble des biens mis
en location par le contribuable, dont les revenus locatifs sont soumis à la RAS. Ainsi,
un contribuable qui dispose de plusieurs biens immeubles dont les revenus locatifs
sont soumis à la RAS, doit souscrire une seule demande d’option dont une copie du
récépissé doit être remise à tous ses locataires chargés d’opérer ladite RAS.
Pour mettre fin à l’option précitée, les contribuables concernés doivent souscrire une
demande, par procédé électronique auprès de l’administration fiscale contre récépissé,
selon un modèle établi à cet effet. Ils doivent également remettre une copie dudit
récépissé à toutes les personnes chargées d’opérer la retenue à la source au moins 15
jours avant la date de l’échéance du versement du loyer du mois qui suit celui de dépôt
de la demande précitée.
   C. Dispense de la déclaration annuelle du revenu global
L’article 86 du CGI a été complété par un nouvel alinéa 6° afin de dispenser les
contribuables disposant des revenus fonciers de l’obligation de souscrire la déclaration
annuelle du revenu global, pour la partie de ces revenus soumise à la retenue à la
source au taux libératoire de 20%.
A ce titre, il est précisé que les revenus fonciers qui n’ont pas été soumis à la RAS au
taux libératoire de 20%, doivent être déclarés dans la déclaration annuelle du revenu
global et régularisés selon les taux du barème progressif.
   D. Obligation de retenue à la source au taux libératoire
L’article 160 bis du CGI a été complété par de nouvelles dispositions qui prévoient
l’obligation de la retenue à la source au taux de 20% au titre des revenus fonciers
versés aux contribuables qui ont opté pour l’imposition prévue à l’article 64-IV dudit
code selon ce taux libératoire.
Cette retenue à la source est effectuée sur la base du revenu foncier brut imposable
des immeubles donnés en location, constitué par le montant brut total des loyers
augmenté des dépenses incombant normalement au propriétaire ou à l'usufruitier et
mises à la charge des locataires et diminué des charges supportées par ledit
propriétaire ou usufruitier pour le compte des locataires et ce, conformément aux
dispositions de l’article 64-I du CGI.
A ce titre, il est précisé que la retenue à la source précitée s’applique aux revenus
bruts fonciers imposables, sans application ni de l’abattement forfaitaire de 40% prévu
à l’article 64-II du CGI, ni du seuil d’exonération de 40 000 dirhams.



                                          21
Date d’effet :
Les dispositions des articles 64-IV, 73 (II-F-12°), 86-6° et 160 bis du CGI, telles que
modifiées et complétées par le paragraphe I de l’article 8 de la LF 2025, sont
applicables aux revenus fonciers encaissés à compter du 1er janvier 2025.
N.B : Pour bénéficier de l’imposition selon le taux libératoire au titre de l’ensemble des
revenus fonciers encaissés au titre de l’année 2025, les contribuables concernés
doivent souscrire la demande d’option auprès de l’administration fiscale contre
récépissé et remettre une copie dudit récépissé à l’ensemble de leurs locataires chargés
d’opérer la retenue à la source avant le versement du premier loyer au titre de l’année
2025.
Néanmoins, en cas de souscription de la demande d’option par un contribuable après
le versement du premier loyer de l’année 2025 et de prélèvement par une société X
de la retenue à la source au titre de ce mois au taux de 10% ou 15%, il est admis, par
tolérance administrative au cours de cette période transitoire, que ce contribuable
demande à la société X d’effectuer une régularisation sur les revenus fonciers versés
ultérieurement, afin que l’ensemble des retenues à la source au titre des revenus
fonciers de l’année 2025 soient effectuées selon le taux libératoire de 20%.
Ledit contribuable bénéficiera ainsi de la dispense de l’obligation de souscrire la
déclaration annuelle du revenu global, pour les revenus fonciers qui ont été soumis
effectivement à la retenue à la source au taux libératoire de 20%.
A défaut, les revenus fonciers qui n’ont pas été soumis à la RAS au taux libératoire de
20% devront être déclarés dans la déclaration annuelle du revenu global et soumis
aux taux du barème progressif.
Exemples d’illustration :
Exemple n° 1 :
Un contribuable marié, ayant trois enfants à charge, dispose au titre de l’année 2025
des revenus suivants :
      un revenu salarial net imposable de 120 000 DH dont le montant de l’impôt
       retenu à la source est de 16 800 DH, sachant que ce revenu est payé par un
       seul employeur ;
      des revenus fonciers bruts imposables de 144 000 DH (soit 12 000 DH par mois)
       provenant de la location d’un magasin commercial à une société « X ».
Cas 1 : Option à l’imposition des revenus fonciers selon le taux libératoire
        de 20%
Supposons que le contribuable concerné a opté pour l’imposition libératoire des
revenus fonciers provenant de la location de son magasin commercial selon le taux
libératoire de 20%, en souscrivant le 10 janvier 2025, soit avant le versement du
premier loyer au titre de l’année 2025, une demande d’option, par procédé
électronique, auprès de l’administration fiscale contre récépissé et il a remis le même
jour une copie dudit récépissé à la société « X » et ce, conformément aux dispositions
de l’article 64-IV du CGI.




                                           22
A cet effet, en vertu des articles 160 bis (2ème alinéa) et 174-IV du CGI, la société
« X », ayant accusé réception de la copie du récépissé précité, est tenue :
    -   d’opérer la retenue à la source au titre du revenu foncier brut imposable versé
        au propriétaire selon le taux libératoire de 20%,
    -   et de verser le montant de l’IR correspondant avant l’expiration du mois suivant
        celui au cours duquel ladite retenue a été opérée.
Le cumul des retenues à la source effectuées au cours de l’année au titre des revenus
fonciers est de : (12 000 x 20%) x 12 = 28 800 DH
Dans ce cas et conformément aux dispositions de l’article 86 (2° et 6°) du CGI, le
contribuable susvisé est dispensé de l’obligation de souscrire la déclaration annuelle
du revenu global, du fait qu’il dispose uniquement d’un revenu salarial payé par un
seul employeur et des revenus fonciers soumis à la retenue à la source au taux
libératoire de 20%.
Cas 2 : Imposition des revenus fonciers dans les conditions du droit commun
Supposons que le contribuable concerné n’a pas opté pour l’imposition des
revenus fonciers selon le taux libératoire. Dans ce cas, en vertu des articles 160
bis (1er alinéa) et 174-IV du CGI, la société « X » est tenue :
        -   d’opérer la RAS au taux non libératoire de 15%, au titre du revenu foncier
            brut imposable versé au propriétaire dès lors que le montant annuel des
            loyers dépasse 120 000 DH,
        -   et de verser le montant de l’IR correspondant avant l’expiration du mois
            suivant celui au cours duquel ladite retenue a été opérée.
Le cumul des retenues à la source effectuées au cours de l’année au titre des revenus
fonciers est de :
                             144 000 x 15% = 21 600 DH
Ledit contribuable doit souscrire une déclaration annuelle de son revenu global, avant
le 1er mars 2026, comprenant son revenu salarial et celui foncier soumis à la RAS au
taux non libératoire de 15%.
Ainsi, le montant de l’IR correspondant auxdits revenus est liquidé comme suit :
Détermination de la base imposable :
 - Montant brut annuel imposable du revenu foncier : ……………….………144 000 DH
 - Abattement au titre des revenus fonciers : 144 000 x 40% …….….….. 57 600 DH
 - Montant du revenu foncier net imposable : 144 000 – 57 600 …...…….86 400 DH
 - Montant du revenu salarial net imposable : ………………………...…..…...120 000 DH
 - Revenu global net imposable : 120 000 + 86 400 …….….....…… 206 400 DH
Calcul de l’impôt dû :
 - Impôt brut : (206 400 x 37%) – 27 400 ……………………..……………..….. 48 968 DH
 - Réduction pour charge de famille (marié ayant trois enfants) : 500 x 4= 2 000 DH
 - Montant de l’IR retenu à la source : 16 800 + 21 600 ………….……………..38 400 DH
 - Impôt à payer : 48 968 – 2 000 – 38 400 ………….……………….……..…. 8 568 DH

                                           23
A cet effet, il est à préciser que le contribuable susvisé est tenu de verser
spontanément, dans le même délai que la déclaration annuelle de son revenu global
susvisée, le montant de l’IR correspondant ainsi calculé.
Exemple n° 2 :
Soit un contribuable marié ayant deux enfants à charge et disposant au titre de l’année
2025 des revenus ci-après :
       revenu salarial net imposable de 170 000 DH dont le montant de l’impôt retenu
        à la source est de 34 300 DH ;
       revenus fonciers bruts imposables de 324 000 DH provenant de la location :
         - d’un appartement à un établissement public « X » de 144 000 DH, soit
           36 000 DH par trimestre ;
         - d’un magasin commercial à une société « Y » de 96 000 DH, soit 8 000 DH
           par mois ;
         - et d’un appartement à usage d’habitation à un particulier de 84 000 DH.
A ce titre, il est à préciser que le contribuable concerné a opté en février 2025 pour
l’imposition de l’ensemble de ces revenus fonciers soumis à la RAS (loyers provenant
des biens immeubles donnés en location à l’établissement public X et à la société Y)
selon le taux libératoire de 20%, en souscrivant une demande d’option, par
procédé électronique, auprès de l’administration fiscale contre récépissé et ce,
conformément aux dispositions de l’article 64-IV du CGI.
Ledit contribuable a remis la copie dudit récépissé à l’établissement public X. Toutefois,
il n’a pas remis cette copie à la société Y.
A cet effet, l’établissement public X a opéré la retenue à la source au titre du revenu
foncier brut imposable versé à la fin de chaque trimestre au propriétaire selon le taux
libératoire de 20% et il a versé le montant de l’IR correspondant au Trésor et ce,
conformément aux dispositions des articles 160 bis (2ème alinéa) et 174-IV du CGI.
Le cumul des retenues à la source effectuées par cet établissement public au cours de
l’année est de :
                           (36 000 x 20%) x 4 = 28 800 DH
La société « Y », n’ayant pas reçu la copie du récépissé de la demande d’option
précitée, a opéré la RAS au taux non libératoire de 10% au titre du revenu foncier
brut imposable versé au propriétaire dès lors que le montant annuel des loyers ne
dépasse pas 120 000 DH et elle a versé le montant de l’IR correspondant et ce,
conformément aux dispositions des articles 160 bis (1er alinéa) et 174-IV du CGI.
Le cumul des retenues à la source effectuées par la société Y au cours de l’année :
                            (8 000 x 10%) x 12 = 9 600 DH
Le contribuable concerné doit souscrire une déclaration annuelle de son revenu global,
avant le 1er mars 2026, au titre de :
-   son revenu salarial,
-   son revenu foncier soumis à la RAS au taux non libératoire de 10%,
-   ainsi que son revenu foncier non soumis à la RAS (bien loué par un particulier) :


                                           24
Détermination de la base imposable :
 - Montant brut annuel imposable du revenu foncier soumis à la RAS au taux non
   libératoire de 10% : ……………………………….……………………………...………96 000 DH
 - Montant brut annuel imposable du revenu foncier non soumis à la RAS : 84 000 DH
 Ainsi, le montant brut annuel imposable des revenus fonciers est de :
                            96 000 + 84 000 = 180 000 DH
 - Abattement au titre des revenus fonciers : 180 000 x 40% ……….…..….. 72 000 DH
 Soit un montant du revenu foncier net imposable de :
                           180 000 – 72 000 = 108 000 DH
 - Montant du revenu salarial net imposable …………………….………..……...170 000 DH
Ainsi, le revenu global net imposable est de :
                          170 000 + 108 000 = 278 000 DH


Calcul de l’impôt dû :
 - Impôt brut : (278 000 x 37%) – 27 400 ……………………………………….. 75 460 DH
 - Réduction pour charge de famille (marié ayant deux enfants) : 500 x 3= 1 500 DH
 - Montant de l’IR retenu à la source au titre du revenu salarial et du revenu foncier
   soumis au taux non libératoire : 34 300 + 9 600 ……………………………. 43 900 DH
             Impôt à payer : 75 460 – 43 900 – 1 500 = 30 060 DH
A cet effet, il est à préciser que le contribuable susvisé est tenu de verser
spontanément, dans le même délai que la déclaration annuelle de son revenu global
susvisée, le montant de l’IR correspondant ainsi calculé.
Supposant que le contribuable concerné a remis la copie du récépissé de la demande
d’option précitée à la société Y au cours du mois de juillet 2025 et que cette société a
opéré la retenue à la source au titre du revenu foncier brut imposable versé à partir
de ce mois selon le taux libératoire de 20%, ce contribuable sera dispensé de
l’obligation de déclarer la partie de ces revenus fonciers soumise à la retenue à la
source au taux libératoire de 20%.
NB : Les revenus fonciers qui n’ont pas été soumis à la RAS au taux libératoire de
20% devront être déclarés dans la déclaration annuelle du revenu global et soumis à
l’IR aux taux du barème progressif.
Exemple n° 3 :
Un contribuable marié, ayant deux enfants à charge, dispose au titre de l’année 2025
des revenus suivants :
      un revenu salarial net imposable de 250 000 DH dont le montant de l’impôt
       retenu à la source est de 63 600 DH, sachant que ce revenu est payé par un
       seul employeur ;
      des revenus fonciers bruts imposables de 36 000 DH (soit 3 000 DH par mois)
       provenant de la location d’un magasin commercial à une société « Y ».


                                          25
Cas 1 : Option à l’imposition des revenus fonciers selon le taux libératoire
       de 20%
Le contribuable concerné a opté pour l’imposition libératoire des revenus fonciers selon
le taux libératoire de 20%, en souscrivant le 5 janvier 2025 une demande d’option, par
procédé électronique, auprès de l’administration fiscale contre récépissé et il a remis
le même jour une copie dudit récépissé à la société « Y ».
A cet effet, la société « Y », ayant accusé réception de la copie du récépissé précité,
est tenue en vertu des articles 160 bis (2ème alinéa) et 174-IV du CGI :
    -   d’opérer la retenue à la source au titre du revenu foncier brut imposable versé
        au propriétaire selon le taux libératoire de 20%,
    -   et de verser le montant de l’IR correspondant avant l’expiration du mois suivant
        celui au cours duquel ladite retenue a été opérée.
Le montant des retenues à la source effectuées au cours de l’année 2025 au titre des
revenus fonciers est de : (3 000 x 20%) x 12 = 7 200 DH
Dans ce cas, et conformément aux dispositions de l’article 86 (2° et 6°) du CGI, le
contribuable susvisé est dispensé de l’obligation de souscrire la déclaration annuelle
du revenu global, du fait qu’il dispose uniquement d’un revenu salarial payé par un
seul employeur et des revenus fonciers soumis à la retenue à la source au taux
libératoire de 20%.
Cas 2 : Non option à l’imposition des revenus fonciers selon le taux
      libératoire de 20%
Le contribuable en question n’a pas opté pour l’imposition des revenus fonciers
selon le taux libératoire. Dans ce cas, la société « Y » est dispensée de l’obligation
d’opérer la RAS au titre du revenu foncier versé au propriétaire, dès lors que le montant
annuel des loyers ne dépasse pas le seuil exonéré de 40 000 DH et ce, conformément
aux dispositions du 3ème alinéa de l’article 160 bis du CGI.
Dans ce cas, ledit contribuable doit souscrire la déclaration annuelle de son revenu
global, avant le 1er mars 2026, comprenant le revenu salarial et foncier.
Ainsi, le montant de l’IR correspondant auxdits revenus est liquidé comme suit :
Détermination de la base imposable :
 - Montant brut annuel imposable du revenu foncier : ………………….…… 36 000 DH
 - Abattement au titre des revenus fonciers : 36 000 x 40% …….…...….. 14 400 DH
 - Montant du revenu foncier net imposable : 36 000 – 14 400 …...……. 21 600 DH
 - Montant du revenu salarial net imposable : ……………………….…..…... 250 000 DH
 - Revenu global net imposable : 21 600 + 250 000 …………......…… 271 600 DH
Calcul de l’impôt dû :
 - Impôt brut : (271 600 x 37%) – 27 400 ……………………………………..….. 73 092 DH
 - Réduction pour charge de famille (marié ayant deux enfants) : 500 x 3= 1 500 DH
 - Montant de l’IR retenu à la source au titre du revenu salarial :…….……..63 600 DH
 - Impôt à payer : 73 092 – 1 500 – 63 600 ………………………..………..…. 7 992 DH


                                           26
A cet effet, il est à préciser que le contribuable susvisé est tenu de verser
spontanément, dans le même délai que la déclaration annuelle de son revenu global
susvisée, le montant de l’IR correspondant ainsi calculé.
4- Création d’une nouvelle catégorie de revenus imposables en matière d’IR
Avant l’entrée en vigueur de la LF 2025, le champ d’application de l’IR ne permettait
pas d’appréhender certains revenus des personnes physiques qui ne se rattachent pas
à l’une des cinq catégories de revenus et profits soumis à cet impôt, tels que prévus à
l’article 22 du CGI, à savoir :
        - les revenus professionnels ;
        - les revenus provenant des exploitations agricoles ;
        - les revenus salariaux et revenus assimilés ;
        - les revenus et profits fonciers ;
        - les revenus et profits de capitaux mobiliers.
Afin d’assurer l’équité fiscale, la LF 2025 a complété l’article 22 précité par un nouvel
alinéa « 6° », pour créer une nouvelle catégorie de revenus imposables à l’IR dite « les
autres revenus et gains » qui permet d’appréhender les autres revenus et gains
imposables qui ne relèvent pas de l’une des cinq catégories de revenus précitées et
ce, conformément aux bonnes pratiques internationales.
Dans ce sens, la LF précitée a complété le CGI par un nouvel article 70 bis qui définit
les autres revenus et gains pour l’application de l’impôt sur le revenu. Cet article prévoit
que cette nouvelle catégorie comprend les revenus et gains, qui ne relèvent pas de
l’une des catégories visées à l’article 22 (1° à 5°) du CGI, suivants :
   -     les revenus évalués dans le cadre de la procédure de l’examen de l’ensemble
         de la situation fiscale des personnes physiques dont la source n’a pas été
         justifiée ;
   -     les gains de jeux de hasard par internet de source étrangère quelle que soit leur
         forme ;
   -     les revenus et gains divers provenant des opérations lucratives qui ne relèvent
         pas d’une autre catégorie de revenus.
       A- Revenus évalués dans le cadre de la procédure de l’examen de
          l’ensemble de la situation fiscale des personnes physiques dont la
          source n’a pas été justifiée
Il est rappelé que la LF 2024 avait complété l’article 30 du CGI par l’alinéa 4°, afin de
préciser que sont considérés comme revenus professionnels pour l’application de
l’impôt sur le revenu, les revenus évalués dans le cadre de la procédure de l’examen
de l’ensemble de la situation fiscale des personnes physiques dont la source n’a pas
été justifiée.
Suite à la création de la nouvelle catégorie de revenus imposables à l’IR, la LF 2025 a
reclassé ces revenus dans cette nouvelle catégorie « Autres revenus et gains ».
A cet effet, l’article 8-III de la LF 2025 a abrogé l’alinéa 4° de l’article 30 du CGI précité.
De même, les dispositions faisant référence à ces revenus ont été supprimées au
niveau des articles 34 et 39 du même code.


                                              27
Il est à rappeler que l’imposition des revenus évalués précités, dans le cadre de
l’examen de l’ensemble de la situation fiscale des particuliers, ne donne pas lieu à un
redressement en matière de TVA ou de taxe professionnelle.
       B- Les gains de jeux de hasard par internet de source étrangère
La LF 2025 a institué l’obligation de retenue à la source (RAS) sur les gains de jeux de
hasard par internet de source étrangère.
Les gains de jeux de hasard s’entendent de tous les gains des jeux dont le
fonctionnement repose totalement ou partiellement sur le hasard, quelle que soit leur
nature ou leur forme.
A ce titre, la LF 2025 a introduit les modifications suivantes :
    Obligation de retenue à la source et de versement
Les dispositions de la LF 2025 ont complété le CGI par un nouvel article 160 ter en vue
d’instituer l’obligation d’opérer, pour le compte du Trésor, une retenue à la source au
taux libératoire de 30% prévu à l’article 73-II-G-9° dudit code, par les
établissements de crédit et organismes assimilés ou toute autre personne qui
verse ou intervient dans le paiement des gains de jeux de hasard par internet de source
étrangère.
Cette retenue à la source est appliquée sur le montant total brut des gains versés,
sans aucune déduction.
Le montant de cette retenue à la source doit être versé à l’administration fiscale par
les personnes précitées par procédé électronique, selon un modèle établi par
l’administration, avant l’expiration du mois suivant celui au cours duquel la retenue à
la source a été opérée, conformément aux dispositions de l’article 174-VII du CGI.
    Obligation de déclaration des gains de jeux de hasard par internet de
     source étrangère
Les personnes chargées d’opérer la RAS sur les gains de jeux de hasard par internet
de source étrangère, doivent souscrire par procédé électronique auprès de
l’administration fiscale, avant le 1er mars de chaque année, une déclaration au titre
desdits gains, conformément aux dispositions de l’article 154 quater du CGI telles
qu’ajoutées par la LF 2025.
Cette déclaration doit comporter, pour chaque bénéficiaire des gains précités, les
indications suivantes :
   -     le prénom et nom ;
   -     le numéro de la carte nationale d’identité électronique ou la carte de séjour ou
         le numéro d’identification fiscale ;
   -     le montant brut des gains versés ;
   -     le montant de la retenue à la source correspondante.
    Régularisation de l’impôt retenu à la source
La LF 2025 a complété les dispositions de l’article 186-A du CGI, afin de prévoir que la
majoration de 20% applicable en cas de rectification de la base imposable est portée
à 30% pour les contribuables soumis à l’obligation de RAS sur les gains de jeux de
hasard par internet de source étrangère.


                                              28
Cette LF 2025 a également complété les dispositions de l’article 222-A du CGI relatives
à la procédure de rectification du montant de l’impôt retenu à la source, que celui-ci
résulte d’une déclaration ou d’une régularisation pour défaut de déclaration, en vue de
préciser que la RAS sur les gains de jeux de hasard par internet de source étrangère
est également soumise à cette procédure de rectification.
    Sanctions pour infraction en matière de déclaration et de versement
La LF 2025 a complété le CGI par un nouvel article 203 ter qui prévoit que les
établissements de crédit et organismes assimilés ou toute personne qui verse ou
intervient dans le paiement des gains de jeux de hasard par internet de source
étrangère qui n’ont pas souscrit ou ont souscrit hors délai la déclaration des gains
précités, encourent les majorations prévues à l’article 184 dudit code calculées sur le
montant de l’impôt retenu ou qui aurait dû être retenu.
En cas de déclaration incomplète ou comportant des éléments discordants, les
majorations précitées sont calculées sur le montant de l’impôt retenu ou qui aurait dû
être retenu et correspondant aux omissions et inexactitudes relevées.
De même, la LF 2025 précitée a complété les dispositions de l’article 208 du CGI
relatives aux sanctions pour paiement tardif des impôts, droits et taxes pour prévoir
qu’en cas de défaut de versement ou de versement hors délai du montant de l’impôt
retenu à la source visé à l’article 160 ter du même code, la pénalité de 10% est portée
à 20%.
    Taxation d’office pour défaut de déclaration
La LF 2025 a complété l’article 228-I (1° et 3°) du CGI, afin de prévoir que la procédure
de taxation d’office pour défaut de déclaration s’applique lorsque :
   -   les personnes chargées d’opérer la retenue à la source sur les gains de jeux de
       hasard par internet de source étrangère ne produisent pas dans les délais
       prescrits la déclaration au titre desdits gains prévue à l’article 154 quater du
       même code ;
   -   les personnes susvisées n’effectuent pas ou ne versent pas au Trésor les
       retenues à la source au titre de ces gains, dont elles sont responsables,
       conformément aux dispositions de l’article 160 ter dudit code.
    Procédure pour l’application des sanctions en cas de déclaration ne
     comportant pas certaines indications
La LF 2025 a également complété l’article 230 bis du CGI, afin de prévoir que la
procédure d’application des sanctions en cas de déclaration ne comportant pas
certaines indications est également applicable lorsque la déclaration des gains de jeux
de hasard par internet de source étrangère prévue à l’article 154 quater du CGI ne
comporte pas les indications prévues par cet article qui n’ont pas d’incidence sur la
base imposable ou sur le montant de l’impôt.
A ce titre, il est rappelé que le contribuable concerné est invité par lettre dans les
formes prévues à l'article 219 du code précité, à compléter sa déclaration dans un délai
de 15 jours suivant la date de réception de ladite lettre.
Si le contribuable susvisé ne complète pas sa déclaration dans le délai précité,
l'administration l’informe par lettre, dans les formes prévues à l'article 219 précité, de
l'application des sanctions prévues à l’article 184 du CGI.


                                           29
NB : Il convient de rappeler que les dispositions susvisées concernent les gains de
jeux de hasard par internet de source étrangère soumis à l’IR par voie de retenue à la
source.
Les titulaires des gains de jeux de hasard de source étrangère n’ayant pas subi de
retenue à la source, demeurent tenus de souscrire la déclaration annuelle de revenu
global au titre de leurs revenus de source étrangère, conformément aux dispositions
des articles 25 et 82 du CGI, sous réserve des conventions fiscales tendant à éviter la
double imposition.
S’agissant des gains de jeux de hasard de source marocaine, il convient de signaler
que la LF 2025 a institué une contribution sociale de solidarité sur les bénéfices des
entreprises de jeux de hasard qui sera détaillée dans le VIII de la présente note
circulaire.
De ce fait, les titulaires des gains de jeux de hasard de source marocaine ne sont pas
tenus de souscrire une déclaration ou de verser un impôt au titre de ces gains.
    C- Revenus et gains divers provenant des opérations lucratives qui ne
       relèvent pas d’une autre catégorie de revenus
L’article 70 bis-3° du CGI a inclus dans la définition de la nouvelle catégorie des autres
revenus et gains soumis à l’IR, prévue au 6° de l’article 22 du CGI, tous les revenus et
gains divers provenant des opérations lucratives qui ne relèvent pas d’une autre
catégorie de revenus.
Il s’agit notamment des revenus non spécifiés et des profits divers occasionnels,
provenant des opérations ayant un caractère lucratif effectuées avec l’intention de
générer un revenu ou de réaliser un profit.
La qualification d'un revenu ou gain divers imposable reste liée aux circonstances de
sa réalisation, à sa nature et à son origine.
Ainsi, n’entrent pas dans cette catégorie, les sommes encaissées à l’occasion d’un acte
civil exercé dans des circonstances et conditions ne lui conférant pas un caractère
lucratif, telles que les sommes versées par les parents à leurs enfants pour la prise en
charge des études ou d’autres frais, les donations entre ascendants et descendants, la
vente occasionnelle par un particulier (non commerçant) d’un bien meuble d’occasion,
etc.
Toutefois, si un particulier réalise des opérations d’achat-revente de biens neufs ou
d’occasion ou réalise des prestations de services, même à titre occasionnel, dans
l’intention de réaliser un profit, ledit profit pourrait être imposable dans le cadre de la
catégorie des autres revenus et gains, lorsqu'il n'entre pas dans la catégorie des
revenus professionnels.
Il est à préciser, à ce titre, que les revenus de source étrangère des personnes non-
résidentes non imposables au Maroc, ne sont pas concernés par cette nouvelle
catégorie de revenus.
Il est à préciser également que les gains de jeux de hasard de source marocaine ne
sont pas considérés comme des revenus et gains divers, tels que prévus à l’article 70
bis-3° du CGI.




                                            30
        Déclaration d’identité fiscale
La LF 2025 précitée a modifié les dispositions de l’article 78 du CGI pour prévoir
l’obligation pour les contribuables passibles de l’IR au titre des revenus et gains divers
relevant de cette nouvelle catégorie de revenus, prévue au 6° de l’article 22 dudit
code, de souscrire une déclaration d’identité fiscale dans les conditions prévues à
l’article 78 précité et ce, dans les trente (30) jours suivant soit la date du début de leur
activité, soit celle de l'acquisition de la première source de revenu.
En cas d’infraction aux dispositions relatives à la déclaration d’identité fiscale précitée,
une amende de cinq cents (500) dirhams est applicable, conformément aux
dispositions de l’article 201 du CGI telles que complétées par la LF 2025.
        Obligation de déclaration et de versement relative aux revenus et
         gains divers
Les titulaires de ces revenus et gains doivent de manière spontanée :
   -   déclarer leur montant brut dans le cadre de la déclaration annuelle du revenu
       global prévue à l’article 82 du CGI,
   -   et verser le montant de l’IR correspondant, selon les taux du barème progressif
       prévu à l’article 73-I du CGI, conformément aux dispositions de l’article 173-I
       dudit code.
En cas d’infraction aux dispositions relatives à la déclaration ou au versement
susvisées, le contribuable concerné est régularisé conformément aux dispositions
prévues par le CGI à cet effet.
Date d’effet :
 - Les dispositions de l’article 70 bis-3° du CGI, telles qu’ajoutées par le paragraphe
   II de l’article 8 de la LF 2025, sont applicables aux revenus et gains divers acquis
   à compter du 1er janvier 2025.
 - Les dispositions relatives à l’application de la retenue à la source prévues par les
   articles 73 (II-G-9°), 174-VII, 186, 208, 222, 228-I et 230 bis du CGI, telles que
   modifiées et complétées par le paragraphe I de l’article 8 de la LF 2025 et par les
   articles 154 quater, 160 ter et 203 ter dudit code, telles qu’ajoutées par le
   paragraphe II de l’article 8 de la LF 2025, sont applicables aux gains de jeux de
   hasard par internet de source étrangère, versés à compter du 1er juillet 2025.
5- Révision du traitement fiscal des rachats de retraites complémentaires
   dont les cotisations n'ont pas été déduites
Avant l’entrée en vigueur de la LF 2025, les dispositions de l’article 57-9° du CGI
prévoyaient l’exonération des retraites complémentaires souscrites parallèlement aux
régimes visés à l’article 59-II-A dudit code et dont les cotisations n’ont pas été déduites
pour la détermination du revenu net imposable.
Dans le cadre de l’harmonisation du traitement fiscal des contrats d’épargne à long
terme, notamment les contrats d’assurance sur la vie ou de capitalisation, les
dispositions de la LF 2025 ont conditionné le bénéfice de l’exonération des prestations
servies au terme des contrats de retraite complémentaire, dont les cotisations n'ont
pas été déduites, par l’obligation de conclure ces contrats pour une durée égale au
moins à 8 ans.



                                            31
De même, la LF 2025 a complété les dispositions de l’article 57 (9° et 10°) du CGI
pour consacrer qu’en cas de décès ou d’invalidité de la personne concernée, il n’est
pas tenu compte du délai précité, à l’instar de ce qui est prévu dans certains plans
d’épargne à long terme.
La LF précitée a également complété les dispositions de l’article 58-II-D du CGI, afin
de clarifier les modalités d’imposition des prestations servies au titre d’un contrat de
retraite complémentaire, d’assurance sur la vie ou de capitalisation ou d’un contrat
d’investissement Takaful, avant l'expiration de la durée de 8 ans.
A ce titre, il convient de préciser que les prestations relatives auxdits contrats, servies
avant l'expiration de la durée de 8 ans, sont imposables à l’IR, dans les cas ci-après,
par voie de retenue à la source opérée par le débirentier, aux taux du barème
prévu à l’article 73-I du CGI, comme suit :
      Cas de versement d’un capital
La base imposable de la prestation versée sous forme de capital est égale à la
différence entre le montant du capital perçu et le montant des cotisations ou primes
versées par l’assuré correspondant audit capital.
      Cas de versement d’une rente certaine
La base imposable de la prestation versée à l’assuré sous forme de rente certaine, au
titre de chaque période, est égale à la différence entre le montant de la rente à verser
au titre de la période concernée et la quote-part du montant des cotisations versées
afférent à cette période.
      Cas de versement d’une rente viagère
Lorsque la prestation est versée sous forme de rente viagère, celle-ci est imposable
dans les conditions de droit commun, conformément aux dispositions de l’article 60-I
du CGI qui prévoient l’application de l’abattement forfaitaire de :
   -   70% sur le montant brut des rentes viagères qui ne dépasse pas annuellement
       168 000 DH ;
   -   40% pour le surplus.
NB : Il convient de rappeler que le contribuable ayant bénéficié des prestations
susvisées demeure tenu de souscrire la déclaration annuelle du revenu global au titre
desdites prestations, sous réserve des dispositions de l’article 86 du CGI.
Aussi, est-il rappelé que les entreprises d’assurances et les autres débirentiers des
prestations susvisées sont tenus, en sus de l’obligation d’opérer la retenue à la source
de l’impôt correspondant, de souscrire la déclaration des pensions et autres prestations
servies sous forme de capital ou de rente prévue à l’article 81 du CGI et ce, même en
cas de versement de prestations exonérées.
Date d’effet :
Les dispositions des articles 57 (9° et 10°) et 58-II-D du CGI, telles que modifiées et
complétées par le paragraphe I de l’article 8 de la LF 2025, sont applicables aux
prestations servies à compter du 1er janvier 2025.




                                            32
Exemples d’illustration :
Un contribuable marié, ayant deux enfants à charge, a souscrit le 1er mars 2021 un
contrat de retraite complémentaire d’une durée de 8 ans, auprès d’une entreprise
d’assurances, au titre duquel il verse une cotisation mensuelle de 3 500 DH. Ledit
contribuable a opté pour la non déductibilité des cotisations et primes versées.
Exemple n° 1 : Cas des prestations servies à l'expiration de la durée de 8
ans
Après l’écoulement de 8 ans, à compter de la date de la souscription du contrat de
retraite complémentaire dont les cotisations n'ont pas été déduites, l’entreprise
d’assurances verse à l’assuré un capital de 560 000 DH.
Dans ce cas, le capital est exonéré de l’IR et ne fera l’objet d’aucune retenue à la
source par l’entreprise d’assurances, étant donné que la durée de 8 ans est respectée.
Exemple n° 2 : Cas des prestations servies avant la durée de 8 ans
Lorsque le contribuable perçoit une prestation ou procède au rachat de ses cotisations
se rapportant au contrat de retraite complémentaire précité, avant l’écoulement de
huit (8) ans, à compter de la date de la souscription dudit contrat, les prestations
perçues sont imposables aux taux du barème de l’IR, par voie de retenue à la source,
opérée par l’entreprise d’assurances débirentière au titre de l’année de leur versement,
selon les cas suivants :
Cas 1 : Versement d’un capital
Le 1er mars 2025, soit après l’écoulement de 4 ans à compter de la date de la
souscription du contrat, l’assuré en question décide de racheter son capital.
L’entreprise d’assurances lui verse le montant global de ses cotisations revalorisées à
250 000 DH, selon les termes du contrat.
Ce contribuable dispose également d’un revenu salarial net imposable de 190 000 DH
dont le montant de l’impôt retenu à la source s’élève à 41 400 DH.
    Imposition du capital versé par voie de retenue à la source effectuée
     par l’entreprise d’assurances
      -   Montant brut du rachat : ….………………………………..……….250 000 DH
      -   Montant total des cotisations : (3 500 x 12 x 4) …………… 168 000 DH
      -   Montant de la prestation imposable servie :
                250 000 – 168 000…………………………………….………..82 000 DH
      -   Montant de l’IR que l’entreprise d’assurances doit prélever à la source, aux
          taux du barème, après application de la réduction pour charge de famille:
               (82 000 x 30%) – 18 000 – (500 x 3) : ………..…....…. 5 100 DH
    Régularisation de la situation fiscale du contribuable au vu de sa
     déclaration annuelle du revenu global
Dans ce cas, ledit contribuable est tenu de souscrire sa déclaration annuelle du revenu
global et de verser spontanément le montant de l’impôt exigible, avant le 1 er mars
de l’année 2026, comme suit :




                                          33
Détermination de la base imposable :
   -   Montant de la prestation imposable servie …………………………82 000 DH
   -   Montant du revenu salarial net imposable …………….………….190 000 DH
   -   Revenu global net imposable : 82 000 + 190 000 ..…..272 000 DH
Calcul de l’impôt dû :
   -   Impôt brut : (272 000 x 37%) – 27 400 ……………………………..73 240 DH
   -   Réduction pour charge de famille (marié ayant deux enfants) :
                500 x 3 :………………………………………………………..…….. 1 500 DH
   -   Montant de l’IR retenu à la source : 5 100 + 41 400 ……..….....46 500 DH
   -   IR à payer : 73 240 – 1 500 – 46 500 ………………….…..…….. 25 240 DH
Cas 2 : Versement d’une rente certaine
Après l’écoulement de 5 années à compter de la date de la souscription du contrat,
l’assuré en question décide de bénéficier d’une rente certaine sur une période de 4
ans.
    Montant de la prime :………………………………………..……….….…. 3 500 DH
    Durée de cotisation : …………………………………………….…..…….… 5 ans
    Montant total des cotisations : (3 500 x 12) x 5…………..…...210 000 DH
    Nombre d’années de versement de la rente certaine :…………………. 4 ans
    Montant de la rente certaine versée au titre de l’année 2026 : 87 500 DH
    Quote-part du montant des cotisations versées afférent à la période de 4 ans :
            210 000 / 4 :………………………………………………………….……52 500 DH
    Base imposable : 87 500 – 52 500 :……………………..……………… 35 000 DH
Ainsi, les prestations versées dans ce cas ne feront l’objet d’aucune retenue à la source
par l’entreprise d’assurances, étant donné que la base imposable ne dépasse pas le
seuil de la première tranche du barème d’IR exonérée de 40 000 DH.
Néanmoins, la déclaration des pensions et autres prestations servies sous forme de
capital ou de rente prévue à l’article 81 du CGI, à souscrire par ladite entreprise
d’assurances, devra comporter les indications relatives à l’assuré concerné et aux
prestations qui lui ont été servies même en l’absence d’un prélèvement de l’IR.
    Régularisation de la situation fiscale du contribuable au vu de sa
     déclaration annuelle du revenu global
Dans ce cas, ledit contribuable est tenu de souscrire sa déclaration annuelle du revenu
global et de verser spontanément le montant de l’impôt exigible, avant le 1 er mars
de l’année 2027, comme suit :
Détermination de la base imposable :
   -   Montant de la prestation imposable servie …………………………35 000 DH
   -   Montant du revenu salarial net imposable ……………………….190 000 DH
   -   Revenu global net imposable : 35 000 + 190 000 ..…..225 000 DH


                                           34
Calcul de l’impôt dû :
   -   Impôt brut : (225 000 x 37%) – 27 400 ……………………………..55 850 DH
   -   Réduction pour charge de famille (marié ayant deux enfants) :
                500 x 3 :…………………………………………………………….. 1 500 DH
   -   Montant de l’IR retenu à la source : ……………………….….......41 400 DH
   -   IR à payer : 55 850 – 1 500 – 41 400 ………………………….. 12 950 DH
Cas 3 : Versement d’une rente viagère
Un contribuable marié ayant deux enfants à charge ayant souscrit un contrat de
capitalisation, au titre duquel il a versé une cotisation mensuelle de 5 000 DH, a décidé
avant l’expiration du délai de 8 ans de mettre fin à ce contrat et de percevoir ses
prestations sous forme d’une rente viagère.
L’entreprise d’assurances lui verse, à ce titre, une rente viagère mensuelle de
3 000 DH.
Ce contribuable dispose également d’un revenu salarial net imposable de 190 000 DH
dont le montant de l’impôt retenu à la source s’élève à 41 400 DH.
    Traitement de la rente viagère par l’entreprise d’assurances
          Montant brut mensuel versé :….…..……………….………..……… 3 000 DH
          Montant de l’abattement forfaitaire : 3 000 x 70% …….……. 2 100 DH
          Montant net imposable : …………………………..…………..………….900 DH
Ainsi, les prestations versées dans ce cas ne feront l’objet d’aucune retenue à la source
par l’entreprise d’assurances, étant donné que la base imposable ne dépasse pas le
seuil de la première tranche du barème d’IR exonérée de 40 000 DH (soit 3 333,33 DH
par mois).
Néanmoins, la déclaration des pensions et autres prestations servies sous forme de
capital ou de rente prévue à l’article 81 du CGI, à souscrire par ladite entreprise
d’assurances, devra comporter les indications relatives à l’assuré concerné et aux
prestations qui lui ont été servies même en l’absence d’un prélèvement de l’IR.
    Régularisation de la situation fiscale du contribuable au vu de sa
     déclaration annuelle du revenu global
Dans ce cas, ledit contribuable est tenu de souscrire sa déclaration annuelle du revenu
global et de verser spontanément le montant de l’impôt exigible, avant le 1 er mars,
comme suit :
Détermination de la base imposable :
   -   Montant net imposable de la rente servie :(900 x 12)...….……10 800 DH
   -   Montant du revenu salarial net imposable :……………………….190 000 DH
   -   Revenu global net imposable : 10 800 + 190 000 ..…..200 800 DH
Calcul de l’impôt dû :
   -   Impôt brut : (200 800 x 37%) – 27 400 ……………………………..46 896 DH
   -   Réduction pour charge de famille (marié ayant deux enfants) :


                                           35
                 500 x 3 :…………………………………………………………….. 1 500 DH
   -   Montant de l’IR retenu à la source/revenu salarial : ..……......41 400 DH
IR à payer : 46 896 – 1 500 – 41 400 …………………………………….… 3 996 DH
6- Clarification du traitement fiscal applicable aux opérations de transfert
   d’immeubles ou de droits réels immobiliers du patrimoine privé d’une
   personne physique à l’actif de son entreprise
La LF 2025 a complété l’article 61-II du CGI, pour clarifier l’imposition des profits
fonciers réalisés suite au transfert d’immeubles ou de droits réels immobiliers du
patrimoine privé d’une personne physique à l’actif de son entreprise soumise à l’IR
selon le régime du résultat net réel ou simplifié (RNR/RNS), lorsque ledit transfert a
été effectué à une valeur supérieure au prix d’acquisition d’origine desdits
immeubles et droits réels immobiliers.
Ainsi, les opérations de transfert du patrimoine privé au patrimoine professionnel, à
une valeur supérieure au prix d’acquisition, sont considérées comme des opérations
de cession soumises à l’IR au titre des profits fonciers dans les conditions du droit
commun, au sens des dispositions de l’article 61-II (dernier alinéa) du CGI précité.
Aussi, il est précisé que la personne physique concernée est tenue, dans ce cas, de
souscrire la déclaration des profits fonciers dans les 30 jours qui suivent la date de
l’inscription de l’immeuble ou du droit réel immobilier à l’actif de son entreprise en
même temps que le versement spontané de l’impôt y afférent et ce, conformément
aux dispositions des articles 83-I et 173-I du CGI, sous réserve du droit de contrôle de
l’administration prévu à l’article 224 dudit code.
Les dispositions de la LF précitée ont également complété l’article 62-III du CGI, pour
exclure du champ d’application de l’IR au titre des profits fonciers, le transfert
d’immeubles ou de droits réels immobiliers du patrimoine privé d’une personne
physique à l’actif de son entreprise soumise à l’IR, selon le régime du RNR ou celui du
RNS, lorsque ledit transfert a été effectué au prix d’acquisition d’origine desdits
immeubles et droits réels immobiliers.
A ce titre, il convient de rappeler que pour les immeubles acquis par héritage, le prix
d’acquisition d’origine à considérer au sens des dispositions de l’article 65-II du CGI,
sous réserve du droit du contrôle de l’administration, est :
      soit la valeur vénale des immeubles, au jour du décès du de cujus, inscrite sur
       l'inventaire dressé par les héritiers ;
      soit, à défaut, la valeur vénale des immeubles au jour du décès du de cujus, qui
       est déclarée par le contribuable, sans tenir compte des actes de partage ou tout
       autre acte ultérieur à la date du décès du de cujus.
Date d’effet :
Les dispositions des articles 61-II et 62-III du CGI, telles que modifiées et complétées
par le paragraphe I de l’article 8 de la LF 2025, sont applicables aux opérations de
transfert d’immeubles ou de droits réels immobiliers du patrimoine privé d’une
personne physique à l’actif de son entreprise, effectuées à compter du 1er janvier 2025.




                                          36
Exemple d’illustration :
Une personne physique a acquis, en date du 25/05/2000 moyennant un prix
d’acquisition de 1 000 000 DH, un lot de terrain de 300 m².
Le 01/02/2025, ladite personne physique a décidé de procéder au transfert du lot de
terrain précité de son patrimoine privé à l’actif de son entreprise exerçant l’activité de
promotion immobilière soumise à l’IR selon le régime du résultat net réel (RNR).
Cas n°1 : Transfert effectué à une valeur supérieure au prix d’acquisition
d’origine
La personne physique en question a décidé le 01/02/2025 de procéder au transfert du
lot de terrain précité de son patrimoine privé à l’actif de son entreprise à une valeur
d’apport de 2 600 000 DH.
A cet effet, le terrain a été inscrit le 01/02/2025 à l’actif de l’entreprise à 2 600 000 DH,
soit à une valeur supérieure au prix d’acquisition d’origine du bien immeuble précité
de 1 000 000 DH.
Le profit ainsi réalisé à l’occasion dudit transfert est imposable en matière d’IR dans la
catégorie des profits fonciers, conformément aux dispositions de l’article 61-II du CGI.
Ledit profit est déterminé dans les conditions prévues à l’article 65 dudit code.
Détermination du profit foncier (PF) imposable :
   -   Valeur du transfert : ……………………………………….………….…..2 600 000 DH
   -   Prix d’acquisition d’origine :..…………….………………….…….…….1 000 000 DH
   -   Frais d’acquisition : 1 000 000 x 15%......................................150 000 DH
   -   Coût d’acquisition : 1 000 000 + 150 000…………………….……..1 150 000 DH
   -   Application du coefficient de réévaluation
                    1 150 000 x 1,573 ……………….....…………….….……1 808 950 DH
   -   Profit foncier imposable : 2 600 000 – 1 808 950 ………..………...791 050 DH
Calcul de l’IR/PF dû :
   -   L’IR/PF calculé au taux de 20% : 791 050 x 20% .................... 158 210 DH
   -   Cotisation minimale (CM) : 2 600 000 x 3%................................78 000 DH
Ainsi, le montant de l’IR/PF dû est 158 210 DH du fait que l’IR calculé au taux de 20%
est le plus élevé.
Calcul de 5% du prix de cession (Transfert), dès lors que le contribuable n’a
pas demandé l’avis préalable de l’administration fiscale :
   -   2 600 000 x 5% :……………………………………………..………………. 130 000 DH
Vu que le montant de l’IR/PF dû (158 210 DH) est supérieur à 5% du prix de cession
(130 000 DH), le montant de l’impôt à verser, dans ce cas, est de
158 210 DH.
Ainsi, la personne physique concernée est tenue de souscrire la déclaration des profits
fonciers dans les 30 jours qui suivent la date du transfert précité, soit le 01/02/2025
en même temps que le versement spontané de l’impôt ainsi calculé et ce,
conformément aux dispositions des articles 83-I et 173-I du CGI.

                                              37
Cas n°2 : Transfert effectué au prix d’acquisition d’origine
Supposons que la personne physique concernée a effectué le transfert du lot de terrain
susvisé à l’actif de son entreprise à son prix d’acquisition d’origine, soit
1 000 000 DH.
Dans ce cas, ledit transfert n’est pas assujetti à l’IR au titre des profits fonciers et ce,
conformément aux dispositions de l’article 62-III du CGI.
7- Clarification de l’éligibilité des opérations d’apport des actions et parts
   sociales des sociétés à prépondérance immobilière au régime incitatif
   relatif au sursis de paiement de l’IR
Les opérations de cession ou d’apport d’actions ou de parts sociales des sociétés à
prépondérance immobilière non cotées en bourse de valeurs sont soumises à l’IR au
titre des profits fonciers réalisés, à l’instar de tous les biens immeubles et droits réels
immobiliers.
A ce titre, les dispositions de la LF 2025 ont clarifié l’éligibilité des opérations d’apport
desdites actions et parts sociales au régime incitatif prévu à l’article 161 bis –II du CGI
relatif au bénéfice du sursis de paiement de l’IR, au titre des profits fonciers réalisés
lors des opérations d’apport de biens immeubles ou des droits réels immobiliers.
Pour bénéficier dudit sursis, les contribuables ayant effectué l’opération dudit apport
en vertu des dispositions de l’article 161 bis-II précité, doivent souscrire la déclaration
des profits fonciers dans les soixante (60) jours qui suivent la date de l’acte par lequel
l’apport a été réalisé et ce, conformément aux dispositions de l’article 83-II du CGI, tel
que modifié et complété par la LF 2025.
Cette déclaration doit être accompagnée de l’acte par lequel l’apport a été réalisé et
comportant le prix d’acquisition et la valeur des éléments apportés évaluée par un
commissaire aux apports choisi parmi les personnes habilitées à exercer les missions
de commissaire aux comptes.
En cas de non production de l’un des documents susvisés, le profit foncier réalisé suite
à l’opération d’apport précitée, est imposable dans les conditions de droit commun.
Lorsque la société bénéficiaire de l’apport susvisé procède à la cession totale ou
partielle ou au retrait des actions ou de parts sociales des sociétés à prépondérance
immobilière apportées ou lorsque les personnes physiques cèdent les titres acquis en
contrepartie dudit apport, le sursis de paiement précité est levé et l’IR afférent au
profit foncier doit être versé, par procédé électronique, par la personne physique ayant
effectué ledit apport, dans les 30 jours qui suivent la date de cession ou du retrait en
question.
Il est à signaler qu’en cas de cession partielle des actions ou de parts sociales
apportées ou des titres acquis en contrepartie dudit apport, le versement du montant
de l’IR, ayant fait l’objet de sursis de paiement, est effectué au prorata des titres cédés.




                                             38
8- Clarification du principe d’imposition des profits fonciers réalisés dans le
   cadre de la procédure d’expropriation qui résulte d’une voie de fait
Dans le cadre de la clarification et l’amélioration de la lisibilité des textes fiscaux, la LF
2025 a complété les dispositions de l’article 61-II du CGI pour clarifier le principe
d’imposition des profits fonciers réalisés suite à l’expropriation d’immeubles ou des
droits réels immobiliers qui résulte d’une voie de fait (‫ )االعتداء المادي‬ou suite à tout
transfert de propriété en exécution d’une décision judiciaire ayant force de la chose
jugée.
Cette mesure consacre le principe d’équité fiscale, en cas de transfert de la propriété
d’un bien immeuble, quelle que soit la procédure de ce transfert (acte ou jugement)
et ce, afin d’éviter les divergences d’interprétation et le contentieux.
A ce titre, il convient de signaler que le transfert de propriété suite à une décision
judiciaire porte, en plus de l’expropriation pour cause d’utilité publique et celle qui
résulte d’une voie de fait, sur d’autres cas, tels que la vente aux enchères publiques,
la saisie, etc.
Il est à préciser qu’en cas d’expropriation pour cause d’utilité publique ou qui résulte
d’une voie de fait ou en cas de tout transfert de propriété, en exécution d’une décision
judiciaire ayant force de la chose jugée, le prix de cession s'entend du montant total
versé suite à ladite décision judiciaire, conformément aux dispositions de l’article 65
du CGI telles que complétées par la LF 2025.
    Obligation de retenue à la source et de versement
La LF pour l’année budgétaire 2025 a complété le CGI par un nouvel article 160 quater
qui institue l’obligation d’opérer, pour le compte du Trésor, une retenue à la source au
taux de 5% sur le montant total brut versé par les personnes intervenant dans le
paiement des montants versés aux personnes physiques, en exécution d’une décision
judiciaire ayant force de la chose jugée, en cas d’expropriation pour cause d'utilité
publique ou qui résulte d’une voie de fait ou en cas de tout transfert de propriété.
Le montant de cette retenue doit être versé conformément aux dispositions de l’article
174-VIII du CGI, à l’administration fiscale, par les personnes intervenant dans le
paiement des montants précités, avant l’expiration du mois suivant celui au cours
duquel la retenue à la source a été opérée.
Ce versement s’effectue, par procédé électronique, selon un modèle établi par
l’administration.
   Droit d’imputation et de restitution du montant de l’impôt retenu à la
    source
L’article 160 quater précité prévoit la possibilité pour les personnes physiques dont la
propriété a fait l’objet d’expropriation ou de transfert en exécution d’une décision
judiciaire ayant force de la chose jugée, d’imputer le montant retenu à la source sur
l’impôt exigible, avec droit à restitution.
En effet, conformément aux dispositions de l’article 241 bis-I du CGI, telles que
complétées par la LF 2025, lorsque le montant retenu à la source et versé au Trésor
excède celui de l’impôt correspondant au profit foncier réalisé ou constaté en cas
d’expropriation ou en cas de tout transfert de propriété en exécution d’une décision
judiciaire ayant force de la chose jugée, le contribuable concerné bénéficie d’une
restitution d’impôt calculée au vu de la déclaration des profits fonciers prévue à l’article

                                             39
83 du CGI, sous réserve du droit du contrôle de l’administration prévu par les
dispositions de l’article 224 dudit code.
Par ailleurs, les personnes physiques concernées sont tenues de souscrire la
déclaration des profits fonciers précitée, selon un modèle établi par l’administration,
dans les 30 jours qui suivent la date de l'encaissement du montant accordé
conformément aux dispositions de l’article 83-I du CGI tel que modifié par la LF 2025,
en même temps que le versement de l’impôt prévu à l’article 173-I dudit code.
Il est précisé également que les dispositions de l’article 173-I précité ont été
complétées par la LF 2025 pour prévoir l’exclusion des personnes dont la propriété a
fait l’objet d’expropriation ou dont la propriété a été transférée en exécution d’une
décision judiciaire et qui sont soumises à la RAS susvisée, du versement, à titre
provisoire, auprès du receveur de l’administration fiscale de la différence entre le
montant de l’impôt déclaré et 5% du prix de cession.
Date d’effet :
Les dispositions relatives à l’application de la retenue à la source prévues par les
articles 173-I, 174-VIII et 241 bis-I du CGI telles que complétées par le paragraphe I
de l’article 8 de la LF 2025 et par l’article 160 quater dudit code, tel qu’ajouté par le
paragraphe II de l’article 8 de ladite LF, sont applicables aux montants versés à
compter du 1er juillet 2025.
III. MESURES SPECIFIQUES A LA TAXE SUR LA VALEUR AJOUTEE
1- Harmonisation des dispositions relatives aux prestations de services à
   distance avec les bonnes pratiques internationales
Il est à rappeler que, dans le cadre de l’élargissement du champ d’application de la
TVA, la LF 2024 a complété les dispositions de l’article 88 du CGI relatives aux règles
de territorialité, afin d’appréhender les prestations de services fournies à distance de
manière dématérialisée par une personne non résidente n’ayant pas d’établissement
au Maroc à un client ayant son siège, son établissement ou son domicile fiscal au
Maroc, ou à un client résidant à titre occasionnel au Maroc.
Ladite LF 2024 a également complété le CGI par un nouvel article 115 bis, afin
d’instituer l’obligation d’identification des fournisseurs non-résidents desdites
prestations sur une plate-forme électronique ainsi que l’obligation de déclaration du
chiffre d’affaires réalisé et du versement de la taxe due au Maroc via ladite plate-forme.
Dans le cadre de l’harmonisation des dispositions précitées avec les bonnes pratiques
internationales, l’article 8 de la LF 2025 prévoit les modifications suivantes :
   -   la suppression des prestations fournies à distance de manière dématérialisée à
       un client résident à titre occasionnel au Maroc du champ d’application des
       dispositions relatives aux prestations de services fournies à distance de manière
       dématérialisée ;
   -   l’institution d’indicateurs clairs pour définir le domicile fiscal au Maroc des
       acquéreurs de services fournis à distance par les fournisseurs non-résidents ;
   -   la modification de la périodicité du dépôt de la déclaration du chiffre d’affaires
       réalisé au Maroc par les prestataires de services à distance non-résidents.




                                           40
 A- Suppression des prestations fournies à distance de manière
    dématérialisée à un client résident à titre occasionnel au Maroc du
    champ d’application des dispositions relatives aux prestations de
    services fournies à distance de manière dématérialisée
Avant l’entrée en vigueur de la LF 2025, l’article 88 du CGI disposait que l’opération
est réputée faite au Maroc, lorsque la prestation de service est fournie à distance de
manière dématérialisée par une personne non résidente n’ayant pas d’établissement
au Maroc à un client résidant à titre occasionnel au Maroc.
L’article 115 bis du CGI prévoyait, à ce titre, des obligations déclaratives pour les
fournisseurs non-résidents qui fournissent des prestations de services à distance de
manière dématérialisée à des clients résidents à titre occasionnel au Maroc.
Or, selon les meilleures pratiques internationales, le client résident à titre occasionnel
au Maroc doit payer la TVA sur la prestation précitée dans son pays de résidence
habituelle, de même, le client établi au Maroc et résident à titre occasionnel à l’étranger
doit payer cette taxe au Maroc.
Ainsi, afin d’éviter une double taxation et consacrer le principe appliqué dans le cadre
des meilleures pratiques internationales, la LF 2025 a modifié les dispositions des
articles 88-2° et 115 bis du CGI pour supprimer, à compter du 1er janvier 2025, les
prestations fournies à distance de manière dématérialisée par une personne non
résidente n’ayant pas d’établissement au Maroc à un client résident à titre
occasionnel au Maroc.
 B- Institution d’indicateurs clairs pour définir le domicile fiscal au Maroc
    des acquéreurs de services fournis à distance par les fournisseurs non-
    résidents
Conformément aux dispositions de l’article 23-II du CGI, une personne physique est
considérée comme ayant son domicile fiscal au Maroc, au sens du code général des
impôts, lorsqu'elle y dispose de son foyer d'habitation permanent, du centre de ses
intérêts économiques ou lorsque la durée continue ou discontinue de ses séjours au
Maroc dépasse 183 jours pour toute période de 365 jours.
Toutefois, cette définition pose une difficulté pour les prestataires étrangers de
services à distance, dès lors que leurs systèmes d’information ne pourront pas détecter
les clients ayant leur domicile fiscal au Maroc selon la définition susvisée.
Dans le cadre de la simplification et afin de faciliter la conformité fiscale aux
prestataires étrangers soumis aux obligations prévues à l’article 115 bis du CGI, la LF
2025 prévoit, dans l’article 88-2° du CGI, la définition du domicile fiscal au Maroc en
précisant des indicateurs clairs à l’instar des autres pays.
Ainsi, et par dérogation aux dispositions de l’article 23-II du CGI, le client non assujetti
est considéré comme ayant un domicile fiscal au Maroc lorsqu’il acquiert des services
à distance de manière dématérialisée auprès d’un fournisseur non résident, si sa
présence au Maroc est établie selon l’un des indicateurs suivants :
      la présentation par le client au prestataire de services d’une adresse au Maroc
       pour l’émission de la facture ;
      le paiement du prix de la prestation fournie au moyen d’une carte bancaire
       émise par un établissement de crédit ou un organisme assimilé établi au Maroc ;


                                            41
      l’utilisation de l’adresse du protocole internet (IP) au Maroc par le client ;
      l’utilisation de l’indicatif téléphonique international du Maroc par le client.
Ainsi, si l’un des indicateurs susvisés est constaté, la présence du client au Maroc est
confirmée et par conséquent, le fournisseur étranger doit déclarer et verser la TVA sur
la prestation fournie à distance de manière dématérialisée audit client et ce, dans les
conditions prévues à l’article 115 bis du CGI.
 C- Modification de la périodicité du dépôt de la déclaration du chiffre
    d’affaires réalisé au Maroc par les prestataires de services à distance
    non-résidents
Avant l’entrée en vigueur de la LF 2025, les dispositions de l’article 115 bis du CGI
prévoyaient une périodicité mensuelle pour le dépôt de la déclaration du chiffre
d’affaires réalisé au Maroc au titre des prestations de services fournies à distance de
manière dématérialisée aux clients non assujettis établis au Maroc.
Dans le cadre de la simplification des obligations des fournisseurs étrangers et en
harmonisation avec les meilleures pratiques internationales, l’article 8 de la LF 2025
prévoit le dépôt trimestriel de la déclaration du chiffre d’affaires précitée au lieu du
dépôt mensuel.
Ainsi, conformément aux dispositions de l’article 115 bis du CGI, toute personne non
résidente n’ayant pas d’établissement au Maroc, qui fournit des prestations de services
à distance de manière dématérialisée à des clients non assujettis ayant leur siège, leur
établissement ou leur domicile fiscal au Maroc, doit souscrire sur la plateforme
électronique dédiée à cet effet, avant l’expiration du premier mois de chaque
trimestre, la déclaration du chiffre d’affaires réalisé au Maroc au titre des prestations
précitées fournies aux clients non assujettis, autres que ceux ayant opéré la retenue à
la source prévue au 4ème alinéa de l’article 115 du CGI et à l’article 117-III dudit code,
au cours du trimestre précédent et verser, en même temps, la taxe correspondante
sans droit à déduction.
Les modalités d’application des dispositions dudit article 115 bis seront fixées par voie
réglementaire.
2- Révision du régime de la TVA sur les biens d'équipement destinés à
   l'enseignement privé ou à la formation professionnelle
   A- Exonération des biens d'équipement destinés à l'enseignement privé
      ou à la formation professionnelle acquis par les sociétés foncières ou
      les organismes de placement collectif immobilier
Avant l’entrée en vigueur de la LF 2025, les dispositions de l’article 92-I-8° du CGI,
prévoyaient l’exonération de la TVA avec droit à déduction des biens d'équipement
destinés à l'enseignement privé ou à la formation professionnelle, à inscrire dans un
compte d'immobilisation, acquis par les établissements privés d'enseignement ou de
formation professionnelle, à l'exclusion des véhicules automobiles autres que ceux
réservés au transport scolaire collectif et aménagés spécialement à cet effet.
Afin de soutenir l’investissement dans le domaine de l’enseignement et de la formation
professionnelle, l’article 8 de la LF 2025 a prévu l’élargissement de l’exonération
précitée aux biens d’équipement acquis par les sociétés foncières ou les organismes
de placement collectif immobilier (OPCI), créés exclusivement pour la réalisation des


                                            42
projets de construction des établissements privés d'enseignement ou de formation
professionnelle.
Cette exonération est conditionnée par l’accomplissement des formalités
réglementaires prévues à l’article 6-II du décret n° 2-06-574 du 10 hija 1427 (31
décembre 2006) pris pour l’application de la TVA.
En effet, le décret n° 2-24-1110 modifiant et complétant le décret n° 2-06-574 du 10
hija 1427 (31 décembre 2006) pris pour l’application de la TVA, a abrogé et remplacé
les dispositions de l’article 6 dudit décret, afin d’instituer les formalités réglementaires
que les sociétés foncières et les OPCI précités doivent accomplir pour bénéficier de
l’exonération des biens d'équipement destinés à l'enseignement privé ou à la formation
professionnelle.
Ainsi, pour bénéficier de l’exonération de la TVA prévue à l’article 92-I-8° du CGI, les
personnes concernées doivent souscrire une demande d’exonération par procédé
électronique selon un modèle établi par l’administration.
Ladite demande est accompagnée :
     - d’un état descriptif des biens d’équipement destinés à être achetés sur le marché
       intérieur en exonération de la TVA, leur valeur en dirhams ainsi que l’intitulé du
       compte où ils seront inscrits en comptabilité et ce, selon le modèle établi par
       l’administration ;
     - des factures proforma ou devis des travaux indiquant la valeur hors taxe des
       biens d’équipement acquis ainsi que le montant de la TVA dont l’exonération est
       sollicitée.
Après examen de la demande d’exonération, l’administration fiscale délivre, par procédé
électronique, une attestation d’achat en exonération de la TVA. Un exemplaire de
l’attestation est conservé par l’acquéreur et un exemplaire est remis à son fournisseur.
Les factures et tout document se rapportant aux ventes réalisées sous le bénéfice de
l’exonération de la TVA à l’intérieur doivent être revêtus d’un cachet portant la mention
« vente en exonération de la taxe sur la valeur ajoutée en vertu de l’article 92 (I-8°) du
code général des impôts».
En outre, en vertu des dispositions de l’article 102 du CGI tel qu’il a été complété par
l’article 8 de la LF 2025, les obligations de conservation prévues par ledit article
s’appliquent également aux biens d’équipement acquis par les sociétés foncières ou
les OPCI, créés exclusivement pour la réalisation des projets de construction desdits
établissements.
A cet effet, les biens d’équipement acquis par les sociétés foncières ou les OPCI
précités en exonération de la TVA, conformément aux dispositions de l’article 92-I-8°
du CGI, doivent être conservés pendant 60 mois s’il s’agit de biens meubles et pendant
10 années s’il s’agit de biens immeubles.
Date d’effet :
Conformément aux dispositions de l’article 8-IV-15° de la LF 2025, les dispositions de
l’article 92-I-8° du CGI, telles que complétées par le paragraphe I de l’article 8 de LF
2025, sont applicables aux sociétés foncières et aux OPCI qui n’ont pas épuisé le délai
d’exonération fixé à 36 mois avant le 1er janvier 2025.



                                            43
   B- Exclusion du champ d’application de la TVA des locations portant sur
      les locaux non équipés acquis ou construits par des sociétés foncières
      ou des organismes de placement collectif immobilier
L’article 8 de la LF 2025 a modifié les dispositions de l’article 89-I-10°-a) du CGI, afin
d’exclure du champ d’application de la TVA les opérations de location aux
établissements privés d'enseignement ou de formation professionnelle des locaux non
équipés acquis ou construits, avec bénéfice du droit à déduction ou de l’exonération
de la TVA, par les sociétés foncières ou les OPCI visés à l’article 92-I-8° du CGI, créés
exclusivement pour la réalisation des projets de construction desdits établissements.
Par conséquent, les opérations de location aux établissements privés d'enseignement
ou de formation professionnelle de locaux non équipés à usage professionnel, acquis
ou construits avec bénéfice du droit à déduction ou de l’exonération de la TVA par les
sociétés foncières ou les OPCI, créés exclusivement pour la réalisation des projets de
construction desdits établissements, sont situées hors champ d’application de la TVA,
quelle que soit la date de construction ou d’acquisition des locaux précités.
3- Imposition des levures sèches à la TVA au taux de 20% à l’intérieur et à
   l’importation
Avant l’entrée en vigueur de la LF 2025, les levures utilisées dans la panification
produites localement étaient exonérées de la TVA sans droit à déduction, en
application des dispositions de l’article 91 (I-A-1°) du CGI. Parallèlement, les levures
importées utilisées dans la panification bénéficiaient de l’exonération avec droit à
déduction en application des dispositions de l’article 123-1° du CGI.
La non-déductibilité de la TVA à l’intérieur pénalisait les entreprises locales productrices
des levures utilisées dans la panification dans la mesure où la TVA non déduite
constituait un coût additionnel appliqué à l’ensemble des intrants utilisés dans la
production locale desdites levures, tandis que les levures importées bénéficiaient du
droit à déduction dans leurs pays d’origine en tant que produits exportés. Cette
pénalisation concerne essentiellement les levures sèches utilisées dans la panification.
Dans le cadre de l’harmonisation du traitement fiscal à l’intérieur et à l’importation et
en vue d’assurer une concurrence équitable entre le produit importé et le produit local,
la LF 2025 prévoit l’exclusion de la levure sèche utilisée dans la panification des levures
exonérées sans droit à déduction prévues par l’article 91-I-A-1° du CGI.
Par conséquent, à compter du 1er janvier 2025, la levure sèche, quelle que soit son
utilisation, est soumise à la TVA au taux de 20%, à l’intérieur et à l’importation.
Rappel des obligations transitoires
Conformément aux dispositions de l’article 125-II du CGI, à titre dérogatoire et
transitoire, toute personne nouvellement assujettie à la taxe sur la valeur ajoutée, est
tenue de déposer avant le 1er mars de l’année de l’assujettissement au service local
des impôts dont elle relève, l’inventaire des produits, matières premières et emballages
détenus dans le stock au 31 décembre de l’année précédente.
La taxe ayant grevé lesdits stocks antérieurement au 1 er janvier de l’année en cours
est déductible de la taxe due sur les opérations de ventes imposables à ladite taxe,
réalisées à compter de la même date, à concurrence du montant desdites ventes.




                                            44
La taxe sur la valeur ajoutée ayant grevé les biens prévus à l’article 102 du CGI et
acquis par les contribuables visés au premier alinéa ci-dessus, antérieurement au 1er
janvier de l’année en cours n’ouvre pas droit à déduction.
De même, en vertu des dispositions de l’article 125-III du CGI, à titre transitoire et par
dérogation aux dispositions de l’article 95 du CGI, les sommes perçues à compter du
1er janvier 2025 par les contribuables assujettis à compter de cette date, en paiement
des ventes entièrement exécutées et facturées avant cette date, sont soumises au
régime fiscal applicable à la date d’exécution de ces opérations.
Par ailleurs, et conformément aux dispositions de l’article 125-IV du CGI, les assujettis
à la TVA selon le régime de l’encaissement, concernés par les dispositions précédentes,
doivent adresser avant le 1er mars 2025 au service local des impôts dont ils relèvent
une liste nominative des clients débiteurs au 31 décembre 2024, en indiquant pour
chacun d’eux le montant des sommes dues au titre des affaires exonérées sans droit
à déduction à la date d’exécution des opérations de ventes précitées.
NB : Il est à rappeler que pour les assujettis effectuant concurremment des opérations
taxables et des opérations exonérées sans droit à déduction à partir du 1 er janvier
2025, le montant de la taxe déductible ou remboursable est affecté d'un prorata de
déduction calculé conformément à l’article 104 du CGI.
Ledit prorata est déterminé par l'assujetti à la fin de chaque année civile à partir des
opérations réalisées au cours de ladite année. Ce prorata est retenu pour le calcul de
la taxe à déduire au cours de l'année suivante.
A cet effet, pour le calcul du prorata de déduction au titre de l’année 2025, les
entreprises concernées doivent calculer le prorata de déduction à partir des opérations
réalisées au cours de l’année 2024, selon le régime fiscal applicable auxdites opérations
à partir du 1er janvier 2025.
4- Exonération de la viande fraîche ou congelée assaisonnée de la TVA sans
   droit à déduction
Avant l’entrée en vigueur de la LF 2025, les dispositions de l’article 91-I-A-6° du CGI
exonéraient de la TVA sans droit à déduction, la viande fraîche ou congelée.
La LF 2025 prévoit l’élargissement de l’exonération de la viande fraîche ou congelée
de la TVA sans droit à déduction en vue d’inclure la viande assaisonnée.
Ainsi, à compter du 1er janvier 2025, la viande fraîche ou congelée assaisonnée ou non
assaisonnée est exonérée de la TVA sans droit à déduction, conformément aux
dispositions de l’article 91-I-A-6° du CGI.
On entend par « viande fraîche ou congelée assaisonnée », tout type de viande crue
d’animaux de boucherie ou de volailles, fraîche ou congelée, entière, découpée ou
hachée, qui a été préparée avec divers assaisonnements pour en rehausser la saveur.
Il s’agit d’un traitement de ladite viande fraîche à l’aide d’un mélange d’épices (sel,
poivre, paprika, gingembre, cannelle,…) et/ou d’herbes (thyms, origan, basilic,
marjolaine, romarin, persil,…) et/ou d’huile, de sauces, de jus de citron, d’ail, d’oignon
ou d’autres légumes.
Ces assaisonnements ou additifs ont pour finalité l’enrichissement du goût de la viande
avant sa cuisson ou sa consommation et font garder à la viande fraîche toutes ses
caractéristiques.


                                           45
Ainsi, les produits à base de viande obtenus à l’aide de moyens industriels ou faisant
l’objet d’une présentation commerciale ne sont pas concernés par l’exonération prévue
à l’article 91-I-A-6° du CGI et demeurent soumis à la TVA dans les conditions du droit
commun. On peut citer, à titre d’exemple, les nuggets, le « merguez », les saucisses,
le « cordon bleu », les boulettes de viandes au fromage, etc.
De même, sont exclus de la catégorie des viandes fraîches ou congelées les viandes
ayant subi des transformations, telles que le séchage, le salage, le fumage ou la
cuisson.
Toutefois, il est à rappeler que les opérations de vente desdits produits, qui ne
bénéficient pas de l’exonération précitée, réalisées par les commerçants dont le chiffre
d'affaires taxable réalisé au cours de l'année précédente est inférieur à 2 000 000 de
dirhams sont situées hors champ d’application de la TVA, en application des
dispositions de l’article 89-I-2°-b du CGI.
Rappel des obligations transitoires
En vertu des dispositions de l’article 125-III du CGI, à titre transitoire et par dérogation
aux dispositions de l’article 95 du CGI, les sommes perçues à compter du 1 er janvier
2025 par les contribuables exonérés à compter de cette date, en paiement de ventes
entièrement exécutées et facturées avant cette date, sont soumises au régime fiscal
applicable à la date d’exécution de ces opérations.
Par ailleurs, et conformément aux dispositions de l’article 125-IV du CGI, les assujettis
à la TVA selon le régime de l’encaissement, concernés par les dispositions précédentes,
doivent adresser avant le 1er mars 2025 au service local des impôts dont ils relèvent
une liste nominative des clients débiteurs au 31 décembre 2024, en indiquant pour
chacun d’eux le montant des sommes dues au titre des affaires soumises au taux de
la TVA en vigueur à la date d’exécution des opérations de ventes précitées.
La taxe due par les contribuables au titre des affaires visées ci-dessus sera acquittée
au fur et à mesure de l’encaissement des sommes dues.
A cet effet, il y a lieu de préciser que lesdits contribuables doivent continuer à souscrire
leurs déclarations périodiques de TVA comportant le chiffre d’affaires exonéré et le
chiffre d’affaires taxable relatif aux ventes entièrement exécutées et facturées avant
le 1er janvier 2025.
NB : Il est à rappeler que, conformément aux dispositions de l’article 101-1° du CGI,
la TVA qui a grevé les éléments du prix d'une opération imposable est déductible de la
TVA applicable à cette opération. Les assujettis opèrent globalement l'imputation de la
TVA et doivent procéder à une régularisation lorsque l'opération n'est pas
effectivement soumise à la taxe.
De même, pour les assujettis effectuant concurremment des opérations taxables et
des opérations exonérées sans droit à déduction à partir du 1 er janvier 2025, le
montant de la taxe déductible ou remboursable est affecté d'un prorata de déduction
calculé conformément à l’article 104 du CGI.
Ledit prorata est déterminé par l'assujetti à la fin de chaque année civile à partir des
opérations réalisées au cours de ladite année. Ce prorata est retenu pour le calcul de
la taxe à déduire au cours de l'année suivante.
A cet effet, pour le calcul du prorata de déduction au titre de l’année 2025, les
entreprises concernées doivent calculer le prorata de déduction à partir des opérations

                                            46
réalisées au cours de l’année 2024, selon le régime fiscal applicable auxdites opérations
à partir du 1er janvier 2025.
5- Augmentation de la part minimale du produit de la TVA affectée aux
   budgets des collectivités territoriales
Avant l’entrée en vigueur de la LF 2025, la part minimale du produit de la TVA affectée
aux budgets des collectivités territoriales était fixée par les lois de finances à 30 %,
après déduction, sur le produit de la taxe perçue à l'intérieur, des remboursements et
des restitutions prévus par le CGI, et ce, en vertu des dispositions de l’article 125-I
dudit code.
Dans le cadre de la mise en œuvre des dispositions de la loi-cadre n° 69.19 portant
réforme fiscale, visant le renforcement de la contribution de la fiscalité de l’État dans
la promotion du développement territorial et la consolidation de la justice spatiale et
afin d’améliorer les ressources des collectivités territoriales, la LF 2025 prévoit
l’augmentation de la part minimale du produit de la TVA allouée aux budgets des
collectivités territoriales de 30% à 32%.
6- Exonération temporaire de la TVA sur les opérations d’importation de
   certains animaux vivants et produits agricoles
L’augmentation des prix de certains produits alimentaires constatée ces dernières
années, en raison notamment du déficit hydrique dû à la sécheresse, a conduit à une
hausse des coûts de production.
Dans le but d’assurer un approvisionnement normal du marché national à des prix
convenables, la LF 2025 prévoit l’introduction d’une mesure temporaire, au titre de
l'année 2025, afin d’exonérer les opérations d’importation de certains animaux vivants
et produits agricoles de la TVA, du 1er janvier 2025 au 31 décembre 2025 et ce, dans
la limite des contingents fixés.
Ainsi, conformément aux dispositions de l’article 247-XXXXII du CGI et par dérogation
aux dispositions de l’article 121 du CGI, sont exonérés de la TVA à l’importation du 1er
janvier au 31 décembre 2025, les opérations d’importation des animaux vivants et
produits suivants :
     les animaux vivants des espèces bovines, ovines, caprines et camélidés, dans la
      limite d’un contingent fixé, respectivement, à cent cinquante mille (150 000)
      têtes, sept cent mille (700 000) têtes, vingt mille (20 000) têtes et quinze mille
      (15 000) têtes ;
     les velles reproductrices et les génisses, dans la limite d’un contingent de vingt
      mille (20 000) têtes pour chaque catégorie ;
     les viandes des animaux des espèces bovines, ovines et caprines, fraîches,
      réfrigérées ou congelées, dans la limite d’un contingent de quarante mille
      (40 000) tonnes ;
     le riz cargo importé par les industriels du secteur, dans la limite d’un contingent
      de cinquante-cinq mille (55 000) tonnes ;
     les huiles d'olive de qualité vierge et extra vierge, dans la limite d’un contingent
      de vingt mille (20 000) tonnes.




                                           47
IV. MESURES SPECIFIQUES AUX DROITS D’ENREGISTREMENT
1- Révision du régime applicable au bail emphytéotique
 A- Clarification de la notion du bail emphytéotique
Avant la loi de finances 2025, l’article 127-I-A-2° du CGI prévoyait que sont
obligatoirement assujettis aux droits d'enregistrement, les actes et conventions portant
bail à rente perpétuelle de biens immeubles, bail emphytéotique, bail à vie et celui
dont la durée est illimitée.
Afin de clarifier les dispositions de l’article 127-I-A-2° précité et d’éviter les divergences
d’interprétation, la LF 2025 a remplacé l’expression « bail emphytéotique » par
« bail dont la durée est supérieure à 10 ans ».
Cette modification a été également introduite au niveau des articles 129-III-13° et
131-19° et 133-I-A-3° du CGI.
 B- Révision de la base imposable du bail dont la durée est supérieure à 10
    ans
Avant l’entrée la LF 2025, l’article 131-19° du CGI prévoyait que la base imposable des
droits d’enregistrement était déterminée, pour les baux emphytéotiques, par un capital
égal à 20 fois la rente ou le prix du loyer annuel, augmenté des charges.
Suite à la modification de l’expression « bail emphytéotique » et son remplacement
par « bail dont la durée est supérieure à 10 ans », la LF 2025 a révisé la base imposable
des droits d’enregistrement des baux dont la durée est supérieure à 10 ans et inférieure
à 20 ans, en précisant que cette base est déterminée par la somme des montants du
loyer correspondant aux années stipulées dans l’acte, augmentée des charges.
En ce qui concerne, les baux dont la durée est égale ou supérieure à 20 ans, leur base
imposable n’a pas été changée. Elle demeure déterminée par un capital égal à 20 fois
la rente ou le prix du loyer annuel, augmenté des charges.
Exemple n° 1 : Bail dont la durée est égale ou inférieure à 10 ans
Pour un contrat de bail d’un bien immeuble, pour une durée de 6 ans moyennant un
loyer annuel de 24 000 DH, les droits d'enregistrement dus sont fixés à 200 DH, et ce,
en vertu de l'article 135-II-8° du CGI.
Exemple n° 2 : Bail dont la durée est supérieure à 10 et inférieure à 20 ans
Pour un contrat de bail d’un bien immeuble, pour une durée de 14 ans moyennant un
loyer annuel de 16 000 DH en plus du paiement des charges (frais de réaménagement
et entretien) estimées à 10 000 DH, les droits d'enregistrement sont liquidés comme
suit :
Base imposable : (16 000 x 14) + 10 000 = ……………….. 234 000 DH
Liquidation des droits : 234 000 x 6 % = ……………………… 14 040 DH
Exemple n° 3 : Bail dont la durée est égale ou supérieure à 20 ans
Pour un contrat de bail d’un bien immeuble pour une durée de 45 ans, avec les mêmes
conditions ci-dessus, les droits d'enregistrement sont liquidés comme suit :
Base imposable : (16 000 x 20) + 10 000 = ……….……….. 330 000 DH
Liquidation des droits : 330 000 x 6 % = …………….………… 19 800 DH


                                             48
2- Institution d’une sanction applicable aux professionnels chargés
   d’accomplir la formalité de l’enregistrement par voie électronique
Les dispositions du CGI prévoient l’obligation pour les notaires, les adoul, les experts
comptables et les comptables agréés d’accomplir la formalité de l’enregistrement par
procédé électronique.
Afin de sécuriser les informations communiquées par les professionnels chargés
d’accomplir la formalité de l’enregistrement par voie électronique, la LF 2025 a
complété le CGI par un nouvel article 206 bis, qui prévoit ce qui suit :
      l’application d’une amende de 1000 dirhams aux personnes accomplissant la
       formalité de l’enregistrement par procédé électronique, en cas de non
       renseignement d’informations obligatoires, de renseignement d’informations
       incomplètes ou erronées ou en cas de non transmission de l’acte ou de la
       convention ;
      la détermination des informations devant être déclarées par les personnes
       accomplissant la formalité de l’enregistrement par procédé électronique
       conformément à la législation et la réglementation en vigueur ;
      la non application de l’amende précitée, lorsque la correction des omissions est
       opérée dans le délai de 30 jours, à compter de la date d’enregistrement de l’acte
       ou de la convention.
Il est à préciser que l’amende précitée s’applique lorsque les informations renseignées
ne sont pas conformes à celles figurant dans l’acte. Il s’agit notamment des
informations suivantes :
      le nom et prénom ou la raison sociale des parties à l’acte ;
      l’adresse du domicile fiscal ou le lieu de situation du principal établissement ;
      le numéro de la carte d'identité nationale ou de la carte d'étranger et le numéro
       d'identification fiscale ;
      le numéro de l’inscription à la taxe professionnelle et le numéro d’article de la
       taxe d’habitation et de la taxe de services communaux ;
      la nature des opérations objet de l’acte ;
      le prix ou la valeur estimative exprimés dans l’acte ;
      le numéro du titre foncier et autres informations relatives à l’immeuble objet de
       l’acte (adresse, superficie, nature de l’immeuble, ...) ;
      l'origine de la propriété ;
      la base imposable aux droits d’enregistrement ;
      le tarif ;
      les droits de timbre ;
      le numéro de série de l'acte au registre de consignation.
Date d’effet :
Les dispositions précitées prévues par l’article 206 bis du CGI, telles qu’ajoutées par le
paragraphe II de l’article 8 de la LF 2025, sont applicables aux actes et conventions
enregistrés à compter du 1er janvier 2025

                                           49
Exemple :
Par acte notarié en date du 5 janvier 2025, A vend à B un appartement au prix de
3 000 000 DH.
Le notaire a enregistré ledit acte en date du 26 janvier 2025 sur la base de 300 000
DH au lieu de 3 000 000 DH figurant dans l’acte.
Liquidation des droits d’enregistrement effectuée par le notaire :
300 000 x 4%= 12 000 DH
En date du 20 février 2025, le notaire a déposé la demande de correction d’une
omission au niveau du prix de l’appartement (3 000 000 DH au lieu de 300 000
DH).
Liquidation des droits d’enregistrement               effectuée    par   le   receveur
ordonnateur chargé de l’enregistrement :
Droits dus : 3 000 000 x 4%                = 120 000 DH
Droits déjà versés :                       = 12 000 DH
Droits complémentaires : 120 000-12 000 = 108 000 DH
Dans ce cas, l’amende de 1 000 DH ne s’applique pas, toutefois la pénalité et les
majorations de retard demeurent applicables :
 - Majoration de 5% pour rectification hors délai donnant lieu au paiement de droit
   complémentaire = 108 000 X 5% =        5 400 DH
 - Pénalité pour paiement tardif de 5% = 5 400 DH
 - Majorations de retard de 5%           = 5 400 DH
                                         = 16200 DH
Total des droits complémentaires : 108 000 DH+ 16200 DH = 124 200 DH
3- Institution de l’obligation pour les notaires de transmettre les actes
   portant une signature électronique
Avant l’entrée en vigueur de la loi de finances pour l’année budgétaire 2025, les
dispositions de l’article 137-I du CGI prévoyaient que les notaires doivent présenter au
bureau de l’enregistrement les registres minutes pour visa et transmettre une copie
des actes par procédé électronique.
A l’instar de la procédure de l’inscription aux livres fonciers auprès de l’Agence
Nationale de la Conservation Foncière, du Cadastre et de la Cartographie (ANCFCC)
qui prévoit que le document transmis doit porter une signature électronique sécurisée,
la LF 2025 a complété l’article 137-I précité par l’obligation pour les notaires de
transmettre à l’administration fiscale, par procédé électronique, les actes portant leur
signature électronique.
Date d’effet :
Les dispositions précitées prévues par l’article 137-I du CGI, telles que modifiées et
complétées par le paragraphe I de l’article 8 de la LF 2025, sont applicables aux actes
et conventions enregistrés à compter du 1er janvier 2025.




                                          50
4- Amélioration du mode de contrôle par les conservateurs de la propriété
   foncière des actes enregistrés
Avant l’entrée en vigueur de la LF 2025, l’article 139-I du CGI prévoyait qu’il ne peut
être reçu par le conservateur de la propriété foncière, aux fins d’immatriculation ou
d’inscription sur les livres fonciers, aucun acte obligatoirement soumis à
l’enregistrement, si cet acte n’a pas été préalablement enregistré.
Afin de faciliter le contrôle de l’accomplissement de cette formalité pour les actes
présentés à la conservation foncière, la LF 2025 a complété les dispositions de l’article
139-I précité, pour instituer l’obligation d’accompagner les actes présentés aux
conservateurs de la propriété foncière d’une attestation d’enregistrement délivrée,
selon un modèle établi par l’administration, leur permettant de s’assurer de
l’accomplissement de la formalité d’enregistrement et du paiement des droits
correspondants.
L’attestation précitée concerne tous les actes et écrits présentés à la conservation
foncière qu’ils soient enregistrés par voie électronique ou enregistrés auprès du bureau
de l’enregistrement compétent.
L’attestation de l’enregistrement comporte un « code à réponse rapide » (QR Code)
qui permet de vérifier l’authenticité de l’attestation concernée et de visualiser les
informations relatives à la formalité de l’enregistrement.
Toutefois, si l’attestation de l’enregistrement des actes enregistrés directement auprès
des bureaux de l’enregistrement ne comporte pas un QR code, le cachet de
l’administration fait foi.
Dans le cadre de l’harmonisation, la LF 2025 a également prévu le remplacement de
l’expression « conservateur de la propriété foncière et des hypothèques » par
« conservateur de la propriété foncière ».
Date d’effet :
Les dispositions précitées prévues par l’article 139-I du CGI, telles que complétées par
le paragraphe I de l’article 8 de la LF 2025, sont applicables aux actes et conventions
enregistrés à compter du 1er janvier 2025.
5- Consécration de l’exonération des droits d’enregistrement des opérations
   de mutation à titre gratuit des biens immobiliers, au profit des familles de
   Chouhadas, des militaires mutilés lors des opérations et des militaires
   rapatriés et ralliés
Dans le cadre de la mise en œuvre des Hautes Instructions Royales pour la
régularisation de la situation juridique des immeubles attribués aux familles de
«Chouhadas», la LF 2025 a complété les dispositions de l’article 129-III du CGI par un
nouvel alinéa 20°, en vue de consacrer l’exonération en matière des droits
d’enregistrement pour les actes portant mutation à titre gratuit d’immeubles au profit
des familles de Chouhadas composées des veuves de martyrs et leurs enfants, des
militaires mutilés lors des opérations et des militaires rapatriés et ralliés.
Date d’effet :
Les dispositions précitées prévues par l’article 129 du CGI, telles que modifiées et
complétées par le paragraphe I de l’article 8 de la LF 2025, sont applicables aux actes
et conventions enregistrés à compter du 1er janvier 2025.


                                           51
6- Exonération des actes de constitution des garanties au profit de
   l’administration fiscale relatives à tous les impôts ainsi que les
   mainlevées y afférents
Avant l’entrée en vigueur de la LF pour l’année 2025, les dispositions de l’article 129-
IV (17° et 21°) du CGI prévoyaient l’exonération en matière des droits
d’enregistrement des actes portant :
       cautionnement bancaire ou d’hypothèque produits ou consentis en garantie du
        paiement des droits d’enregistrement, ainsi que les mainlevées délivrées par
        l’inspecteur des impôts chargé de l’enregistrement ;
       hypothèque consentie en garantie du paiement de la taxe sur la valeur ajoutée
        versée par l’Etat, ainsi que la mainlevée délivrée par le receveur de
        l’administration fiscale, tel que prévu à l’article 93-I du CGI.
La LF 2025 a modifié et complété les dispositions de l’article 129-IV-21° du CGI, afin
de prévoir la généralisation de l’exonération des droits d’enregistrement à tous les
actes et écrits relatifs à la constitution des garanties et hypothèques consenties en
garantie du paiement de tous les impôts, taxes et droits prévus par le CGI ainsi qu’à
ceux relatifs aux mainlevées délivrées par l’administration fiscale.
Date d’effet :
Les dispositions précitées prévues par l’article 129-IV-21° du CGI, telles que modifiées
et complétées par le paragraphe I de l’article 8 de la LF 2025, sont applicables aux
actes et conventions enregistrés à compter du 1er janvier 2025.
7- Clarification des droits d’enregistrement applicables aux opérations de
   restructuration des groupes de sociétés
Avant la LF 2025, l’article 135-I-2° du CGI prévoyait que sont enregistrées au droit fixe
de mille (1000) dirhams, les opérations de transfert et d’apport visées à l’article 161
bis du CGI relatif au régime d’incitation fiscale aux opérations de restructuration des
groupes de sociétés et des entreprises.
Ce droit fixe s’applique aux actes portant sur les deux opérations suivantes :
   les opérations de transfert des immobilisations corporelles, incorporelles et
       financières réalisées entre les sociétés soumises à l’IS, membres d’un groupe de
       sociétés, visées au paragraphe I de l’article 161 bis précité ;
   les opérations d’apport de biens immeubles, de droits réels immobiliers ou
       d’actions ou parts sociales dans des sociétés à prépondérance immobilière non
       cotées en bourse des valeurs, réalisées par les personnes physiques à l’actif d’une
       société, visées au paragraphe II de l’article 161 bis précité.
La LF 2025 a clarifié les dispositions de l’article 135-I-2° du CGI, en prévoyant que le
droit d’enregistrement fixe de mille (1000) dirhams s’applique auxdites opérations de
transfert ou d’apport réalisées dans les conditions prévues aux paragraphes I
et II de l’article 161 bis du CGI précités.
A cet effet, le non-respect des conditions de fond visées aux paragraphes I et II de
l’article 161-bis du CGI, entraîne l’application du droit proportionnel, selon les règles
du droit commun, à l’opération de transfert ou d’apport concernée, sans préjudice de
l’application des sanctions éventuelles.



                                            52
Ainsi, en ce qui concerne les opérations de transfert des immobilisations corporelles,
incorporelles et financières entre les sociétés du groupe, prévues par le paragraphe I
de l’article 161-bis du CGI, le droit fixe de mille (1000) dirhams est remis en cause
notamment dans les cas suivants :
   -   le non-respect du seuil des participations détenues par la société mère dans le
       capital social des sociétés membres du groupe ;
   -   l’inscription des immobilisations transférées à un compte autre que l'actif
       immobilisé des sociétés concernées par les opérations de transfert ;
   -   le non-respect de l’obligation de transfert des immobilisations en contrepartie
       de l'octroi des titres de participation dans le capital social de la société membre
       du groupe ayant bénéficié du transfert de ces immobilisations ;
   -   la sortie des sociétés concernées par les opérations de transfert du groupe de
       sociétés.
Par ailleurs, l’application du droit fixe de mille (1000) dirhams n’est pas remise en
cause en cas de non-respect des conditions de forme, en l’occurrence, le retard dans
le dépôt des états ou de la déclaration, visés par les articles 20 bis et 83-II du CGI qui
font renvoi à l’article 161-bis (I et II) du CGI.
V.MESURE SPECIFIQUE A LA TAXE SPECIALE ANNUELLE SUR LES VEHICULES
Prolongation du délai de paiement de la taxe spéciale annuelle sur les
véhicules (TSAV) à 60 jours au lieu de 30 jours pour les véhicules mis en
circulation en cours d’année
Avant l’entrée en vigueur de la LF pour l’année 2025, la TSAV relative aux véhicules
mis en circulation en cours d’année était payée dans les 30 jours suivant la date du
récépissé du dépôt du dossier auprès de l’Agence nationale de la sécurité routière
(NARSA) pour l’obtention de la carte grise.
En vue de réduire les cas de contentieux relatifs au paiement des majorations et
pénalités résultant du retard de la délivrance de ladite carte, concernant les véhicules
mis en circulation en cours d’année, la LF pour l’année 2025 a modifié les dispositions
de l’article 261-I du CGI afin de porter le délai précité de 30 jours à 60 jours.
VI. MESURES COMMUNES
1- Institution d’un régime d’incitation fiscale en faveur des représentations
   de la Fédération Internationale de Football Association (FIFA) au Maroc
   et des organismes qui lui sont affiliés
Dans le cadre de l’accompagnement de la Fédération Internationale de Football
Association (FIFA) pour l’implantation de son bureau régional permanent à Rabat et
pour appuyer le développement de ses activités au Maroc et dans la région, la LF 2025
a institué un régime d’incitation fiscale en faveur de ses représentations au Maroc et
des organismes qui lui sont affiliés, au titre de toutes leurs activités ou opérations
conformes à l’objet défini dans ses statuts.
A ce titre, la LF 2025 a institué en faveur de la FIFA au Maroc et des organismes qui
lui sont affiliés, l’exonération de l’impôt sur les sociétés, de l’impôt sur les revenus
salariaux, de la TVA et des droits d’enregistrement et de timbre.




                                           53
   A- En matière d’IS
    Exonération totale permanente d’IS
L’article 8 de la LF 2025 a complété les dispositions de l’article 6-I-A du CGI par un 36°
alinéa pour préciser que les représentations de la FIFA au Maroc et les organismes qui
lui sont affiliés, créés conformément à la législation et la réglementation en vigueur,
bénéficient de l'exonération totale permanente de l'IS, au titre de l’ensemble de leurs
activités ou opérations conformes à l’objet défini dans ses statuts.
Il a rappelé que l’exonération totale permanente en matière d’IS ouvre droit à une
exonération totale permanente en matière de la cotisation minimale.
Il a été également précisé, dans le dernier alinéa de l'article 6-I-A du CGI, que les
représentations de la FIFA au Maroc et les organismes qui lui sont affiliés bénéficient
aussi :
     - de l’abattement de 100% sur les produits des actions, parts sociales et revenus
       assimilés prévus à l'article 6 (I-C-1°) du CGI ;
     - et de l’exonération des plus-values sur cession de valeurs mobilières.
    Exonération permanente en matière de retenue à la source sur les
     produits des actions, parts sociales et revenus assimilés
L’article 8 de la LF pour l’année 2025 a complété l’article 6 (I-C-1°) du CGI par un
nouvel alinéa qui prévoit l’exonération permanente de la retenue à la source sur les
produits des actions, parts sociales et revenus assimilés, pour les produits provenant
des bénéfices des représentations de la FIFA au Maroc et des organismes qui lui sont
affiliés, versés, mis à la disposition ou inscrits en compte de la FIFA ou des organismes
qui lui sont rattachés.
    Exonération de la retenue à la source sur les produits bruts
L’article 8 de la LF 2025 a complété l’article 6-I-C du CGI par un alinéa 5° qui prévoit
l’exonération permanente de la retenue à la source sur les produits bruts et les
rémunérations analogues visés à l’article 15 du CGI, versés, mis à la disposition ou
inscrits en compte de la FIFA ou de ses organismes affiliés non-résidents, par les
représentations de la FIFA et ses organismes affiliés établis au Maroc.
   B- En matière d’IR
La LF 2025 prévoit l’exonération de l’IR au titre des revenus salariaux et assimilés
versés par les représentations de la FIFA au Maroc et les organismes qui lui sont affiliés
à leur personnel n’ayant pas la nationalité marocaine et ce, conformément aux
dispositions de l’article 57-26° du CGI.
   C- En matière de TVA
La LF 2025 prévoit l’exonération de la TVA, à l’intérieur et à l’importation, des biens,
matériels, marchandises et services acquis ainsi que les opérations réalisées par les
représentations de la Fédération Internationale de Football Association au Maroc et les
organismes qui lui sont affiliés, conformément à l’objet défini dans ses statuts.
Ainsi, à compter du 1er janvier 2025 et conformément aux dispositions de l’article 92-
I-56° du CGI, sont exonérés de la TVA à l’intérieur, les biens, matériels, marchandises
et services acquis ainsi que les opérations réalisées par les représentations de la
Fédération Internationale de Football Association au Maroc et les organismes qui lui
sont affiliés, conformément à l’objet défini dans ses statuts.

                                           54
De même, sont exonérés de la TVA à l’importation conformément aux dispositions de
l’article 123- 60° du CGI, les biens, matériels, marchandises et services importés par
les représentations de la Fédération Internationale de Football Association au Maroc
et les organismes qui lui sont affiliés précités, conformément à l’objet défini dans ses
statuts.
Par ailleurs, les dispositions de l’article 8 de la LF 2025 prévoient également des
modifications au niveau de l’article 124-I du CGI pour instituer la condition
d’accomplissement des formalités prévues par le décret n° 2-06-574 du 10 hija 1427
(31 décembre 2006) pris pour l’application de la taxe sur la valeur ajoutée.
Ainsi, conformément aux dispositions de l’article 8-III du décret n° 2-06-574 précité
tel que modifié et complété par le décret n° 2-24-1110, pour bénéficier de l'exonération
de la TVA prévue à l’article 92-I-56° et à l’article 123 -60° du CGI, la représentation
de la Fédération Internationale de Football Association au Maroc ou l’organisme qui lui
est affilié doit adresser une demande d’exonération, par procédé électronique, selon
un modèle établi par l’administration.
Ladite demande est accompagnée :
    - d’un état descriptif, selon un modèle établi par l’administration, des biens,
     matériels, marchandises et services destinés à être achetés sur le marché intérieur
     ou importés en exonération de TVA et à être utilisés dans le cadre de l'objet
     statutaire de la Fédération Internationale de Football Association ;
    - des factures proforma ou devis des biens, matériels, marchandises et services
     acquis indiquant la valeur en hors taxe ainsi que le montant de la taxe dont
     l’exonération est sollicitée.
Après examen de la demande d’exonération, l’administration fiscale délivre, par procédé
électronique, à la représentation ou l’organisme bénéficiaire, pour les achats à l’intérieur,
une attestation d'achat en exonération de la TVA.
La représentation ou l’organisme bénéficiaire conserve un exemplaire de l'attestation et
de la liste des biens, matériels, marchandises et services exonérés et un exemplaire est
remis à son fournisseur.
Les factures et tous documents se rapportant aux ventes réalisées sous le bénéfice de
l'exonération prévue ci-dessus, doivent être revêtus d'un cachet portant la mention
«vente en exonération de la taxe sur la valeur ajoutée en vertu de l’article 92 (I –56°)
du code général des impôts».
Pour les importations, l’administration fiscale délivre, par procédé électronique, une
attestation d’importation en exonération de la TVA qui est transmise à l’administration
des douanes et impôts indirects.
   D- En matière de DET
La LF 2025 prévoit l’exonération des droits d’enregistrement et de timbre pour tous les
actes et écrits afférents aux activités et opérations réalisées par les représentations de
la Fédération Internationale de Football Association au Maroc et les organismes qui lui
sont affiliés, conformément à l’objet défini dans ses statuts ainsi que les titres de séjour
délivrés aux représentants de la FIFA et aux employés des représentations de la FIFA
au Maroc et les organismes qui lui sont affiliés et ce, conformément aux dispositions
des articles 129-I-5° et 250-I-10° du CGI.


                                             55
Date d’effet :
L’article 8-IV-3 de la LF 2025 a prévu que les dispositions des articles 6, 57, 92, 123,
129 et 250 du CGI, telles que complétées, sont applicables à compter du 1er janvier
2025.
2- Révision du régime des sociétés en participation et des groupements
   d’intérêt économique
  A- Révision du régime des sociétés en participation (SEP)
Avant l’entrée en vigueur de la LF 2025, les SEP étaient exclues du champ d’application
de l’IS, sauf option irrévocable audit impôt, conformément aux dispositions des articles
2-II et 3-1° du CGI.
En cas d'option pour l’IS, les SEP étaient imposées au nom de l'associé habilité à agir
au nom de chacune de ces sociétés et pouvant l'engager et ce, conformément aux
dispositions de l’article 18 du CGI. Toutefois, tous les associés restent solidairement
responsables de l'impôt exigible et, le cas échéant, des majorations et pénalités y
afférentes et ce, conformément aux dispositions de l’article 180-III du CGI.
Lorsque la SEP n’opte pas pour l’IS, les personnes physiques membres de cette SEP
étaient soumises à l’IR individuellement, pour leur part dans le résultat de la SEP,
conformément aux dispositions de l’article 26-II du CGI. Dans ce cas, chaque personne
est tenue de souscrire sa propre déclaration et sa part dans le résultat de la SEP entre
dans la détermination de son propre revenu net professionnel et/ou agricole. De
même, les personnes morales soumises à l’IS associées de ladite SEP, sont tenues de
rapporter à leur résultat fiscal, leur part dans le résultat de la SEP.
Dans le cadre de la rationalisation du régime d’imposition applicable aux SEP, la LF
2025 a introduit plusieurs modifications sur le régime actuel.
 a) Imposition obligatoire à l’IS des SEP comprenant plus de cinq (5)
    associés personnes physiques ainsi que celles comprenant au moins une
    personne morale
La LF 2025 a complété les dispositions de l’article 2-I du CGI par un nouvel alinéa 6°
qui prévoit l’assujettissement obligatoire à l’IS des sociétés en participation
comprenant au moins une personne morale ainsi que celles comprenant plus de cinq
(5) associés personnes physiques.
A ce titre, la LF 2025 a modifié également les dispositions des articles 2-II et 3-1° du
CGI, pour exclure du champ d’application d’IS, les SEP comprenant moins de six (6)
associés et ne comprenant que des personnes physiques, sous réserve de l’option
irrévocable à cet impôt, tel que prévu à l’article 2- II dudit code.
 b) Clarification des modalités d’imposition des SEP soumises à l’IS
Suite à l’intégration des SEP comprenant plus de 5 associés personnes physiques ou
au moins une personne morale dans le champ des personnes obligatoirement passibles
de l’IS, ces sociétés sont devenues comme des entités distinctes fiscalement, ayant
leur propre identifiant fiscal et leur propre résultat fiscal imposable, tout en consacrant
le principe de solidarité entre tous les associés pour le paiement de l’impôt dû.
De même, les bénéfices distribués par ces SEP sont considérés comme des dividendes
soumis à la retenue à la source sur les produits d’actions, parts sociales et revenus
assimilés dans les conditions de droit commun.

                                            56
A ce titre, il a été précisé dans l’article 2-I-6° du CGI que l’imposition est établie au
nom de la société en participation concernée, sous réserve des dispositions relatives à
la solidarité, prévues à l’article 180-III dudit code.
Cet article 180-III a été complété par la référence à l’article 2-I-6° du CGI pour
consacrer ledit principe de solidarité, en vertu duquel tous les associés des SEP
passibles de l’IS restent solidairement responsables de l'impôt exigible et, le cas
échéant, des majorations et pénalités y afférentes.
 c) Institution de l’obligation pour les associés de la SEP soumise à l’IR
    d’accompagner leurs déclarations de certains documents
L’article 26-II du CGI, tel que modifié par les dispositions de la LF 2025, précise que
lorsqu’une personne physique est associée d’une SEP comprenant moins de six (6)
associés personnes physiques n’ayant pas opté pour l’IS, sa part dans le résultat de la
société en participation entre dans la détermination de son revenu net professionnel
et/ou agricole.
L’article 82-I du CGI a été également complété, en prévoyant que la déclaration du
revenu global doit être accompagnée :
       des documents comptables générés par la comptabilité de la SEP qui doit être
        tenue conformément à la législation et la réglementation en vigueur. Ces
        documents comptables comprennent notamment :
        -   le bilan ;
        -   le compte de produits et charges ;
        -   l’état des informations complémentaires ;
       d’un état de répartition du résultat entre les associés faisant ressortir pour
        chacun d’eux :
        -   le nom et le prénom ;
        -   l’adresse ;
        -   le numéro d’identification fiscale ;
        -   la part de l’associé dans le résultat net réalisé par la société en
            participation.
Il est rappelé que conformément aux dispositions de l’article 26-II (dernier alinéa) du
CGI, les contribuables concernés doivent produire un acte authentique ou un contrat
ou tout document en tenant lieu faisant ressortir la part des droits de chacun dans la
société en participation. A défaut, l’imposition est émise au nom de la société en
participation.
Dates d’effet :
 - L’article 8-IV-1 de la LF 2025 a prévu que les dispositions des articles
  2 (I-6° et II), 3-1°, 26-II et 180-III du CGI relatives aux sociétés en participation,
  telles que modifiées et complétées, sont applicables aux exercices ouverts à compter
  du 1er janvier 2026.
 - L’article 8-IV-14 de la LF 2025 a prévu que les dispositions de l’article
  82-I du CGI, telles que modifiées et complétées, sont applicables aux déclarations
  souscrites à compter du 1er janvier 2025.


                                            57
  B- Révision du régime des groupements d’intérêt économique (GIE)
Avant l’entrée en vigueur de la LF 2025, l’article 3-4° du CGI consacrait le principe de
la transparence fiscale au profit des GIE, en les excluant du champ d’application de
l’IS. Cependant, le résultat dégagé au titre de l’exercice de leur activité était
appréhendé au niveau de leurs membres.
En effet, conformément aux dispositions de l’article 8-V du CGI, le résultat fiscal de
chaque exercice comptable des personnes morales membres d’un groupement
d'intérêt économique, comprend, le cas échéant, leur part dans les bénéfices réalisés
ou dans les pertes subies par ledit groupement.
Dans le cadre de l’harmonisation avec le régime d’imposition des SEP, la LF 2025 a
complété les dispositions de l’article 2-I par un nouvel alinéa 7°, afin d’intégrer les GIE
dans le champ d’application de l’IS, en précisant que leur imposition demeure établie
au nom des personnes morales et physiques membres de ces groupements, à
concurrence de leur quote-part dans le résultat net desdits groupements.
A cet effet, plusieurs mesures d’harmonisation ont été adoptées, à savoir :
  l’abrogation des dispositions excluant les GIE du champ d’application de
   l’IS
Suite à l’intégration des GIE dans le champ d’application de l’IS, l’article 8-III de la LF
2025 a abrogé les dispositions de l’article 3-4° du CGI qui les excluaient de ce champ
d’application.
  la clarification des modalités d’imposition des GIE constitués de
   personnes physiques
La LF 2025 a complété les dispositions de l’article 26-II du CGI pour prévoir que
lorsqu’une personne physique est membre d’un GIE, sa part dans le résultat dudit GIE
entre dans la détermination de son revenu net professionnel et/ou agricole.
  l’institution de l’obligation de dépôt de l’état de répartition du résultat
   net
La LF 2025 a complété les dispositions de l’article 20-I du CGI, en instituant pour les
GIE l’obligation de joindre à leur déclaration du résultat fiscal, l’état de répartition du
résultat net entre leurs membres faisant ressortir pour chacun d’eux :
    - le prénom et le nom ou la raison sociale ;
    - l’adresse du siège social ou du domicile fiscal ou du principal établissement ;
    - le numéro d’identification fiscale ;
    - la part du membre dans le résultat net réalisé par le groupement d'intérêt
      économique.
Date d’effet :
L’article 8-IV-2 de la LF 2025 a prévu que les dispositions des articles 2-I-7°, 20-I et
26-II du CGI relatives aux GIE, telles que modifiées et complétées, sont applicables
aux exercices ouverts à compter du 1er janvier 2025.




                                             58
3- Prorogation du délai prévu pour bénéficier de l’abattement de 70%
   appliqué sur la plus-value nette réalisée à l’occasion de la cession des
   éléments de l’actif immobilisé
Avant 2025, l’article 247-XXXV du CGI prévoyait une mesure transitoire visant
l’incitation des entreprises à réinvestir le produit de cession de leurs éléments d’actif
immobilisé, au titre des exercices ouverts au cours des années 2022 à 2025.
Cette mesure prévoyait l’application d’un abattement de 70% sur la plus-value nette
réalisée à l’occasion de la cession des éléments de l’actif immobilisé, à l’exception des
terrains et constructions, sous réserve du respect des conditions prévues par l’article
247-XXXV précité.
Dans le cadre de la promotion de l’investissement à long terme créateur de valeur
ajoutée et d’emploi, tel que prôné par la loi-cadre n° 69-19 précitée, la LF 2025 a
prorogé le délai d’application de cette mesure jusqu’à 2030, en prévoyant la
suppression de l’exclusion concernant les terrains et les constructions, afin
d’encourager les sociétés à réinvestir le montant global des produits de cession des
éléments d’actif immobilisé.
A cet effet, les entreprises bénéficient de l’abattement de 70% sur la plus-value nette
réalisée, à compter du 1er janvier 2025, suite à la cession de tous les éléments d’actif
immobilisé, y compris les terrains et les constructions.
Ainsi, les cessions des terrains et constructions effectuées avant le 1er janvier 2025 ne
peuvent pas bénéficier de cet abattement.
Il est rappelé que le bénéfice de l’abattement de 70% précité est accordé sous réserve
du respect des conditions ci-après :
    - le délai écoulé entre la date d'acquisition des éléments concernés par la cession
      et la date de la réalisation de leur cession, doit être supérieur à huit (8) ans ;
    - l’entreprise concernée s’engage à réinvestir le montant global des produits de
      cession net d’impôt en immobilisations, dans un délai de trente-six (36) mois à
      compter de la date de clôture de l’exercice concerné par la cession, selon un
      modèle établi par l’administration à joindre à la déclaration du résultat fiscal
      prévue à l’article 20-I ou 82-I du CGI ;
    - ladite entreprise souscrit à l’administration fiscale un état comprenant le
      montant global des produits de cession net d’impôt ayant fait l’objet du
      réinvestissement et la nature des immobilisations acquises ainsi que la date et
      le prix de leur acquisition, selon un modèle établi par l’administration à joindre
      à la déclaration du résultat fiscal prévue à l’article 20-I ou 82-I du CGI ;
    - l’entreprise concernée conserve les immobilisations acquises pendant au moins
      cinq (5) ans, à compter de la date de leur acquisition.
Par ailleurs, il y a lieu de signaler que les terrains et constructions non affectés à
l’exploitation de l’entreprise ne sont pas éligibles à l’abattement de 70% sur la plus-
value nette précité. C’est le cas notamment de la cession par les établissements de
crédit des actifs immobiliers acquis par dation en paiement et inscrits parmi les
immobilisations hors exploitation, non affectées aux services commerciaux, techniques
et administratifs de l’établissement bancaire.




                                           59
N.B : Il est rappelé que la NC 732 relative aux dispositions de la LF 2022 avait clarifié
les autres règles concernant l’application de ce dispositif qui demeurent inchangées.
4- Révision des modalités d’application de l’impôt retenu à la source sur les
   produits d’actions, parts sociales et revenus assimilés
Avant l’entrée en vigueur de la LF pour l’année budgétaire 2025, l’article 247-XXXVII-
C du CGI prévoyait que le taux de l’impôt retenu à la source de 15% en vigueur au 31
décembre 2022 prévu aux articles 19-IV et 73 (II-C-3°) dudit code sera minoré
progressivement, pour les produits des actions, parts sociales et revenus assimilés
distribués et provenant des bénéfices réalisés au titre de chaque exercice ouvert durant
la période allant du 1er janvier 2023 au 31 décembre 2026, comme suit :
         13,75% au titre de l’exercice ouvert à compter du 1er janvier 2023 ;
         12,50% au titre de l’exercice ouvert à compter du 1er janvier 2024 ;
         11,25% au titre de l’exercice ouvert à compter du 1er janvier 2025 ;
         10% au titre de l’exercice ouvert à compter du 1er janvier 2026.
Le paragraphe XXXVII-C de l’article 247 du CGI précité prévoyait également que les
produits des actions, parts sociales et revenus assimilés distribués et provenant des
bénéfices réalisés au titre des exercices ouverts avant le 1er janvier 2023, demeurent
soumis au taux de 15%.
Les dispositions précitées prévoyaient également que les produits des actions, parts
sociales et revenus assimilés distribués sont considérés avoir été prélevés sur les
exercices les plus anciens.
Dans le cadre de la simplification des modalités d’application progressive de l’impôt
retenu à la source sur les produits des actions, parts sociales et revenus assimilés, la
LF 2025 a modifié les dispositions de l’article 247-XXXVII-C précité pour prévoir
l’application de la retenue à la source auxdits produits distribués comme suit :
         12,50% pour les montants distribués à compter du 1er janvier 2025 ;
         11,25% pour les montants distribués à compter du 1er janvier 2026 ;
         10% pour les montants distribués à compter du 1er janvier 2027.
Ces taux s’appliquent aux produits des actions, parts sociales et revenus assimilés
distribués à compter du 1er janvier 2025, quel que soit l’exercice de leur provenance
et ce, sous réserves des exonérations de la retenue à la source prévues à l’article 6-I-
C du CGI.
Exemple d’illustration :
La société « A », créée le 02/06/2013, est une société de droit marocain soumise à l’IS
dont le capital est détenu entièrement par des personnes physiques.
La situation des bénéfices pouvant faire l’objet de distribution par la société se présente
comme suit :
        Bénéfice de l’exercice 2022 mis en réserve facultative : ……400 000 DH
        Report bénéficiaire de l’exercice 2023 : ………………………..1 000 000 DH
        Bénéfice net comptable de l’exercice 2024 : ………………….1 500 000 DH



                                            60
Suite à une assemblée générale ordinaire tenue le 15/06/2025, ladite société a décidé
la distribution au profit de ses actionnaires d’un montant de 2 500 000 DH.
Pour l’application de la retenue à la source suite aux modifications introduites par la
LF 2025, l’exercice de provenance des bénéfices n’est pas pris en considération.
A ce titre, le montant des bénéfices distribués aux actionnaires de la société « A » est
soumis au nouveau taux de la retenue à la source de 12,50%.
Ainsi, le montant de l’impôt retenu à la source dû est égal à :
2 500 000 x 12,50% = 312 500 DH.
5- Clarification de la notification électronique
Avant l’entrée en vigueur de la LF 2025, les dispositions de l’article 219-II du CGI
prévoyaient que la notification peut « également » être effectuée par voie électronique
à l’adresse électronique communiquée à l’administration fiscale par le contribuable.
Toutefois, l’expression « également » précitée pouvait laisser entendre que la
notification électronique est un moyen secondaire de notification pouvant être utilisé
parallèlement à la notification habituelle.
Dans le but d’éviter les divergences d’interprétation, la LF 2025 a clarifié les
dispositions de l’article 219-II précité, en supprimant l’expression « également » et en
précisant qu’outre les formes de notification habituelles, la notification peut être
effectuée par procédé électronique, conformément à la législation et la réglementation
en vigueur et que cette notification produit les mêmes effets juridiques que la
notification habituelle.
Par ailleurs, la LF 2025 a supprimé le renvoi au texte réglementaire prévu à l’article
145-X du CGI qui devait fixer les modalités d’application de tenue de l’adresse
électronique, vu que la loi n° 43-20 relative aux services de confiance pour les
transactions électroniques et son décret d’application n° 2-22-687, ont déjà prévu les
modalités de tenue d’une adresse électronique auprès d’un prestataire de services de
confiance.
6- Encadrement de la procédure d’accord à l’amiable entre l’administration
   et le contribuable
Dans le cadre de la consolidation de la confiance partagée entre l’administration fiscale
et les usagers, tel que recommandé par la loi-cadre n° 69-19 portant réforme fiscale,
la LF 2025 a institué au niveau de l’article 221 ter du CGI un cadre juridique clair pour
la conclusion des accords à l’amiable entre l’administration fiscale et les contribuables
au cours des procédures fiscales.
Les procédures fiscales concernées sont les procédures prévues par le CGI,
notamment, la vérification de comptabilité, l’examen de l’ensemble de la situation
fiscale des personnes physiques, le contrôle des prix ou déclarations estimatives, les
procédures de dépôt de la déclaration rectificative, la rectification en matière de profits
fonciers, la procédure de taxation d’office, etc.
A cet effet, l’accord peut être conclu après l’engagement des procédures précitées. En
cas de contrôle fiscal, l’accord ne peut être conclu qu’après envoi de la première lettre
de notification.




                                            61
La LF 2025 précitée a prévu que cet accord est définitif et irrévocable et qu’il porte sur
les questions de fait relatives aux éléments d’imposition évalués par l’administration et
ne peut en aucun cas porter sur des questions de droit.
A cet effet, sont considérées comme des questions de fait, les appréciations et les
évaluations effectuées par l’administration fiscale pour la détermination des
bases d’imposition, dans le cadre de l’exercice de son pouvoir d’appréciation, sans
remettre en cause les principes de droit prévus par la législation fiscale en vigueur.
Il s’agit, notamment, des questions de fait afférentes aux rectifications effectuées par
l’administration fiscale compte tenu des informations à sa disposition et des
circonstances de fait liées aux opérations réalisées et à la situation de l’entreprise
concernée.
C’est ainsi que constituent des questions de fait, à titre d’illustration, les rectifications
des montants déclarés relatifs, notamment, aux éléments suivants :
     - le montant du chiffre d’affaires et autres produits imposables évalué par
        l’administration, en dehors de ceux recoupés ;
     - le montant évalué des charges d’exploitation et autres charges déductibles ;
     - les prix d’acquisition et de cession des biens ainsi que les profits, plus-values
        et marges réalisées, estimés par l’administration ;
     - la valeur des avantages en nature ;
     - la valeur des dons et libéralités déductibles ;
     - le reclassement d’une charge en immobilisation ;
     - l’évaluation des bénéfices indirectement transférés entre entreprises ayant
        directement ou indirectement des liens de dépendance ;
     - l’évaluation des bases et des montants des retenues à la source ;
     - les prix déclarés ou estimés, exprimés dans les actes et conventions ;
     - les amortissements et provisions.
Par contre, est considérée comme une question de droit, toute rectification qui porte
sur le principe d’imposition ou d’exonération d’une personne, d’une opération, d’un
acte ou d’un produit ou de déductibilité d’une charge, eu égard aux principes de droit
prévus par la législation et la réglementation fiscale en vigueur et entrainant un
manque à gagner réel et définitif pour le Trésor.
Il s’agit, à titre d’exemple, des rectifications relatives aux principes suivants :
     - le principe de déductibilité d’une charge ou d’imposition d’un produit ou d’une
        opération, selon les conditions prévues par le CGI ;
     - le droit au bénéfice d’un régime fiscal incitatif ou d’un avantage fiscal ;
     - la détermination du taux d’imposition d’un produit, profit, opération ou acte.
Par ailleurs, il convient de signaler que l’accord susvisé constitue le règlement définitif
de la procédure engagée, aussi bien pour les points portant sur les questions de droit
que sur les questions de fait.




                                             62
Il y a lieu de préciser, à cet effet, que les droits en principal afférents aux éléments
d’imposition relatifs à des questions de droit ne peuvent faire l’objet d’aucun
arrangement, compromis ou négociation. Toutefois, en cas d’éléments nouveaux
dûment justifiés, l’administration peut les prendre en considération dans le cadre de
l’accord.
A ce titre, il est précisé que les sanctions afférentes aux éléments notifiés, peuvent
faire l’objet de remise ou modération, au vu des circonstances invoquées, et ce, aussi
bien en ce qui concerne les questions de droit que celles de fait.
Cet accord est rédigé en double exemplaire, selon un modèle établi par
l’administration, et comporte notamment :
      le montant des bases imposables et des droits dus, objet de cet accord ;
      le nom et la qualité des signataires ;
      la date de signature de l’accord.
La LF 2025 a également prévu que cet accord doit être accompagné d’une lettre de
désistement du contribuable de tout recours devant la commission locale de taxation,
la commission régionale du recours fiscal, la commission nationale de recours fiscal,
l’administration fiscale et les tribunaux.
Par ailleurs, en cas de jugement définitif ayant acquis force de chose jugée, l’accord à
l’amiable précité ne peut porter sur un montant de droits inférieur à celui fixé dans ce
jugement. Toutefois, lorsque le jugement ne s’est pas prononcé sur des redressements
portant sur des questions de fait, ces redressements peuvent faire l’objet d’un accord
à l’amiable.
7- Élargissement des attributions des commissions locales de taxation (CLT)
Avant l’entrée en vigueur de la LF pour l’année 2025, les compétences des CLT se
limitaient aux recours afférents aux rectifications en matière de revenus professionnels
déterminés selon le régime de la contribution professionnelle unique, de revenus et
profits fonciers et des droits d’enregistrement et de timbre.
La LF pour l’année 2025 a introduit dans l’article 22-6° du CGI une nouvelle catégorie
de revenus imposables en matière de l’IR intitulée « autres revenus et gains » et a
inclus dans la définition de ces revenus prévue à l’article 70 bis du CGI, tous les revenus
et gains divers provenant des opérations lucratives qui ne relèvent pas d’une autre
catégorie de revenus.
Afin de clarifier la commission compétente en matière de recours présentés par les
contribuables au titre desdits revenus et gains divers provenant des opérations
lucratives qui ne relèvent pas d’une autre catégorie de revenus, la LF pour l’année
2025 a modifié les dispositions de l’article 225-I du CGI pour élargir les attributions
des CLT aux recours relatifs aux rectifications portant sur ces revenus et gains.
Par ailleurs, le domicile fiscal du contribuable a été ajouté au niveau de l’article 225-I
précité comme critère de détermination de la CLT compétente pour le recours.




                                            63
VII. CODIFICATION DES TAXES PARAFISCALES
   Intégration des dispositions relatives à la taxe spéciale sur le ciment
    au niveau du CGI
La taxe spéciale sur le ciment a été instituée par l’article 12 de la LF 2002 avec un taux
qui a été fixé initialement à 0,05 dirham par kilogramme de ciment, puis il a été
augmenté à 0,10 et à 0,15 dirham respectivement par l’article 18 de la loi de finances
2004 et l’article 10 de la loi de finances 2012.
Dans le cadre de la mise en œuvre des objectifs de la loi-cadre n° 69-19 portant
réforme fiscale visant la rationalisation et la simplification des règles d’assiette et de
recouvrement de la parafiscalité, l’article 8-II de la LF 2025 a intégré les dispositions
régissant la taxe spéciale sur le ciment dans le titre VII du livre III du CGI (articles
293, 294, 295, 296 et 297).
L’intégration de cette taxe dans le CGI vise notamment :
      l’attribution de la gestion de cette taxe à la Direction Générale des Impôts (DGI),
       pour le ciment produit localement et à l’Administration des Douanes et Impôts
       Indirects (ADII) pour le ciment importé ;
      l’application des règles de recouvrement, de contrôle, de contentieux, de
       sanctions et de prescription prévues par le CGI à la taxe sur le ciment produit
       localement ;
      l’application des règles prévues en matière de douane pour la liquidation et la
       perception de la taxe sur le ciment importé ainsi que pour la constatation des
       infractions, l’application des sanctions et l’engagement des poursuites.
Le produit de cette taxe reste affecté comme par le passé au compte d’affectation
spéciale intitulé « Fonds de solidarité habitat et intégration urbaine ».
   A- Opérations taxables
Conformément aux dispositions de l’article 293 du CGI, la taxe spéciale sur le ciment
s’applique au ciment produit localement ou à l'importation.
La gestion de la taxe spéciale sur le ciment produit localement est attribuée à la DGI
et la gestion de la taxe sur le ciment à l’importation incombe à l’ADII, conformément
aux dispositions du CGI.
   B- Liquidation
En application des dispositions de l’article 294 du CGI, la taxe appliquée au ciment
produit localement est liquidée par les entreprises de production du ciment sur la base
des quantités de ciment vendues et celles utilisées pour leur consommation interne
comme matières intermédiaires.
Pour le ciment importé, la taxe est liquidée comme en matière de douane.
   C- Taux de la taxe
Le taux de la taxe est fixé à 0,15 dirham par kilogramme de ciment, conformément
aux dispositions de l’article 295 du CGI.




                                           64
   D- Obligations de déclaration et de versement
En vertu des dispositions de l’article 296 du CGI, les entreprises de production du
ciment sont tenues de souscrire spontanément auprès de l’administration fiscale, par
procédé électronique, une déclaration selon un modèle établi par l’administration
précisant, notamment, les quantités de ciment vendues et celles utilisées pour la
consommation interne comme matières intermédiaires, au plus tard à la fin du mois
suivant celui de la facturation des ventes de ciment ou de son utilisation pour la
consommation interne.
Ces entreprises doivent verser la taxe spontanément, auprès de l’administration fiscale,
par procédé électronique, dans le même délai précité de déclaration.
   E- Recouvrement, contrôle, contentieux, sanctions et prescription
Conformément aux dispositions de l’article 297 du CGI, les dispositions relatives au
recouvrement, au contrôle, au contentieux, aux sanctions et à la prescription, prévues
dans le CGI, s’appliquent à la taxe spéciale sur le ciment produit localement.
Pour le ciment importé, cette taxe est perçue, les infractions constatées et réprimées
et les poursuites engagées comme en matière de douane.
   F- Abrogation
Le paragraphe III de l’article 8 de la LF 2025 a prévu qu’à compter du 1er janvier 2025,
l’article 12 de la loi de finances n° 44-01 pour l'année budgétaire 2002, tel que modifié
et complété, relatif à la taxe spéciale sur le ciment est abrogé.
Toutefois, les dispositions de cet article demeurent applicables pour les besoins
d’assiette, de recouvrement, de contrôle et de contentieux de cette taxe concernant la
période antérieure à cette date.
   G- Date d’effet
Le paragraphe IV-21 de l’article 8 de la LF 2025 a prévu que les nouvelles dispositions
des articles 293 à 297 du CGI, telles qu’ajoutées par le paragraphe II de cet article 8 de
la LF 2025, sont applicables à compter du 1er janvier 2025.
VIII. CONTRIBUTION SOCIALE DE SOLIDARITE SUR LES BENEFICES DES
      ENTREPRISES DE JEUX DE HASARD
La LF 2025 a complété le CGI par les articles 298 à 303 afin d’instituer une contribution
sociale de solidarité sur les bénéfices des entreprises de jeux de hasard mise à la
charge des établissements qui versent ces gains.
Ladite contribution est calculée au taux de 2% sur la base du même montant du
bénéfice net servant pour le calcul de l’impôt sur les sociétés ou de l’impôt sur le
revenu déterminé d’après le régime du résultat net réel ou celui du résultat net
simplifié.
En ce qui concerne les entreprises de jeux de hasard exerçant en même temps une
autre activité, ladite contribution ne s’applique qu’à la partie du bénéfice correspondant
à l’activité de jeux de hasard.

                                    
"""
    conversation_history = StreamlitChatMessageHistory()  # Créez l'instance pour l'historique

    st.header("Explorez le rapport sur les mesures fiscales de la Loi de Finances 2025 à travers notre chatbot 💬")
    
    # Load the document
    #docx = 'PLF2025-Rapport-FoncierPublic_Fr.docx'
    
    #if docx is not None:
        # Lire le texte du document
        #text = docx2txt.process(docx)
        #with open("so.txt", "w", encoding="utf-8") as fichier:
            #fichier.write(text)

        # Afficher toujours la barre de saisie
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)
    selected_questions = st.sidebar.radio("****Choisir :****", questions)
        # Afficher toujours la barre de saisie
    query_input = st.text_input("", key="query_key",placeholder="Posez votre question ici...", help="Posez votre question ici...")
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)

    if query_input and query_input not in st.session_state.previous_question:
        query = query_input
        st.session_state.previous_question.append(query_input)
    elif selected_questions:
        query = selected_questions
    else:
        query = ""
    predefined_question = "Donnez-moi un résumé du rapport"

    loading_message = st.empty()

    if query :
        st.session_state.conversation_history.add_user_message(query) 
        # Vérifier si la question de l'utilisateur contient la question prédéfinie
        if predefined_question.lower() not in query.strip().lower():
        # Afficher le message de "Génération de la réponse" si la question est différente
            loading_message.text("Génération de la réponse...")
            st.markdown('<div class="loading-message"></div>', unsafe_allow_html=True)

        

        if "Donnez-moi un résumé du rapport" in query:
            summary="""La Note Circulaire n° 736 présente les principales mesures fiscales introduites par la Loi de Finances 2025, visant à alléger la charge fiscale, moderniser le cadre fiscal et renforcer la lutte contre la fraude. Parmi les changements notables, on trouve la baisse de l'impôt sur le revenu (IR) avec un relèvement du seuil d'exonération et une réduction du taux marginal, l'exonération progressive des pensions de retraite, ainsi que des ajustements sur l’impôt sur les sociétés (IS) et la TVA, notamment pour encourager l’investissement et la compétitivité des entreprises. De plus, des réformes touchent les droits d’enregistrement, la taxe sur les véhicules et la fiscalité des revenus fonciers, avec une option pour un taux libératoire. Enfin, la loi introduit des mesures spécifiques pour les entités sportives et renforce la digitalisation des procédures fiscales."""
            st.session_state.conversation_history.add_ai_message(summary) 

        else:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"{query}. Répondre à la question d'apeés ce texte repondre justement à partir de texte ne donne pas des autre information voila le texte donnee des réponse significatif et bien formé essayer de ne pas dire que information nest pas mentionné dans le texte si tu ne trouve pas essayer de repondre dapres votre connaissance ms focaliser sur ce texte en premier: {text} "
                    )
                }
            ]

            # Appeler l'API OpenAI pour obtenir le résumé
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )

            # Récupérer le contenu de la réponse

            summary = response['choices'][0]['message']['content']
           
                # Votre logique pour traiter les réponses
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(response)
            st.session_state.conversation_history.add_ai_message(summary) 
              
            #query_input = ""

            loading_message.empty()


 # Ajouter à l'historique
            
            # Afficher la question et le résumé de l'assistant
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(summary)

            # Format et afficher les messages comme précédemment
                
            # Format et afficher les messages comme précédemment
        formatted_messages = []
        previous_role = None
        if st.session_state.conversation_history.messages:
        # Parcourir les messages de manière inversée par paire (question, réponse)
            messages_pairs = zip(reversed(st.session_state.conversation_history.messages[::2]), 
                             reversed(st.session_state.conversation_history.messages[1::2]))

            for user_msg, assistant_msg in messages_pairs:
                role_user = "user"
                role_assistant = "assistant"
            
                avatar_user = "🧑"
                avatar_assistant = "🤖"
                css_class_user = "user-message"
                css_class_assistant = "assistant-message"
 
            # Formater et afficher la question de l'utilisateur et la réponse de l'assistant
                message_div_user = f'<div class="{css_class_user}">{user_msg.content}</div>'
                message_div_assistant = f'<div class="{css_class_assistant}">{assistant_msg.content}</div>'

                avatar_div_user = f'<div class="avatar">{avatar_user}</div>'
                avatar_div_assistant = f'<div class="avatar">{avatar_assistant}</div>'

                formatted_message_user = f'<div class="message-container user"><div class="message-avatar">{avatar_div_user}</div><div class="message-content">{message_div_user}</div></div>'
                formatted_message_assistant = f'<div class="message-container assistant"><div class="message-content">{message_div_assistant}</div><div class="message-avatar">{avatar_div_assistant}</div></div>'

                formatted_messages.append(formatted_message_user)
                formatted_messages.append(formatted_message_assistant)
          
        # Afficher les messages formatés
            messages_html = "\n".join(formatted_messages)
            st.markdown(messages_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
