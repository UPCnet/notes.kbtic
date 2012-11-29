# -*- coding: utf-8 -*-
#
# From Notes KBTIC to Plone
# Remember to customize lines 18,19, 32, 33, 35 and 102
#
# Principal URL: All documents by cateogry:
#    https://liszt.upc.es/upcnet/backoffice/manualexp.nsf/BF25AB0F47BA5DD785256499006B15A4
#    Notes://Liszt/C1256E520031DA66/BF25AB0F47BA5DD785256499006B15A4
#

import requests
import logging
import re
import transaction
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

NOTES_USER = ""
NOTES_PASS = ""


class NotesSyncKBTIC():

    def __call__(self):
        ###
        ###

        session = requests.session()

        URL = 'https://liszt.upc.es'
        LOGIN_URL = 'https://liszt.upc.es/names.nsf?Login'
        PATH1 = 'BF25AB0F47BA5DD785256499006B15A4'
        PATH = 'C1256E520031DA66/' + PATH1
        BASE_URL = 'https://liszt.upc.es/%s' % PATH
        TRAVERSE_PATH = '/Upcnet/Backoffice/manualexp.nsf/'
        MAIN_URL = 'https://liszt.upc.es' + TRAVERSE_PATH + PATH1 + '?ReadViewEntries&PreFormat&Start=1&Navigate=16&Count=1000000064&SkipNavigate=32783&EndView=1'

        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename='import-KBTIC.log',
                            level=logging.DEBUG)

        params = {
                    'RedirectTo': '/' + PATH,
                    'Servidor': 'schubert.upc.es/helpaute.nsf/',
                    'Username': '%s' % NOTES_USER,
                    'Password': '%s' % NOTES_PASS,
                 }

        extra_cookies = {
        'HabCookie': '1',
        'Desti': BASE_URL,
        'NomUsuari': '%s' % NOTES_USER,
        'LtpaToken': ''
        }

        # Creating default tree sctructure
        # self.createObject('Folder', self.context, "0 - CONTENIDO DE ESTA BD"),
        # self.createObject('Folder', self.context, "01 - UTILIDADES"),
        # self.createObject('Folder', self.context, "Active Directory"),
        # self.createObject('Folder', self.context, "Actualització de continguts en el Web UPC"),
        # self.createObject('Folder', self.context, "ACUP - Doc6"),
        # self.createObject('Folder', self.context, "Address Book - PAB"),
        # self.createObject('Folder', self.context, "Adminpack"),
        # self.createObject('Folder', self.context, "Adquira"),
        # self.createObject('Folder', self.context, "Altes Estudiants"),
        # self.createObject('Folder', self.context, "Alumni UPC"),
        # self.createObject('Folder', self.context, "Amics"),
        # self.createObject('Folder', self.context, "Antivirus"),
        # self.createObject('Folder', self.context, "Aparador"),
        # self.createObject('Folder', self.context, "ARA"),
        # self.createObject('Folder', self.context, "Archibus"),
        # self.createObject('Folder', self.context, "ARI"),
        # self.createObject('Folder', self.context, "Atenció Immediata"),
        # self.createObject('Folder', self.context, "Atenció telefònica Centraleta UPCnet"),
        # self.createObject('Folder', self.context, "Atenció Usuaris"),
        # self.createObject('Folder', self.context, "Atenea"),
        # self.createObject('Folder', self.context, "Backoffice"),
        # self.createObject('Folder', self.context, "Backups"),
        # self.createObject('Folder', self.context, "Bases de dades bibliogràfiques"),
        # self.createObject('Folder', self.context, "Bi"),
        # self.createObject('Folder', self.context, "Bibliotècnica"),
        # self.createObject('Folder', self.context, "Bizagi"),
        # self.createObject('Folder', self.context, "Blackberry Enterprise Server"),
        # self.createObject('Folder', self.context, "Boyce"),
        # self.createObject('Folder', self.context, "Cacti"),
        # self.createObject('Folder', self.context, "Campus Digital"),
        # self.createObject('Folder', self.context, "Campus Digital - Atenea Mobil"),
        # self.createObject('Folder', self.context, "Campus Digital - Atenea1x1"),
        # self.createObject('Folder', self.context, "Campus Digital - AteneaSaurus"),
        # self.createObject('Folder', self.context, "Campus Digital - Externs"),
        # self.createObject('Folder', self.context, "Campus Digital - Moodle"),
        # self.createObject('Folder', self.context, "Campus Digital - OFA/SDP"),
        # self.createObject('Folder', self.context, "Canal UPC TV"),
        # self.createObject('Folder', self.context, "Canvis de contrasenya"),
        # self.createObject('Folder', self.context, "Carnet UPC"),
        # self.createObject('Folder', self.context, "Carrega Estudiants al PAB EST-UPC"),
        # self.createObject('Folder', self.context, "CAS - Central authentication service"),
        # self.createObject('Folder', self.context, "Catàleg de les biblioteques de la UPC"),
        # self.createObject('Folder', self.context, "CBL"),
        # self.createObject('Folder', self.context, "CCE"),
        # self.createObject('Folder', self.context, "Cerca d'adreces de correu en webs vulnerables a l'spam"),
        # self.createObject('Folder', self.context, "Cercador UPC"),
        # self.createObject('Folder', self.context, "Certificat digital"),
        # self.createObject('Folder', self.context, "Certificats"),
        # self.createObject('Folder', self.context, "Certificats arrels webs UPC / UPCnet"),
        # self.createObject('Folder', self.context, "Circinus"),
        # self.createObject('Folder', self.context, "Clients Externs UPCnet"),
        # self.createObject('Folder', self.context, "CLOUD Privat UPC"),
        # self.createObject('Folder', self.context, "Cluster DN"),
        # self.createObject('Folder', self.context, "CMSW"),
        # self.createObject('Folder', self.context, "Col·laboratoris"),
        # self.createObject('Folder', self.context, "Connexió Remota VNC"),
        # self.createObject('Folder', self.context, "Consoles"),
        # self.createObject('Folder', self.context, "Consulta web administradors del Servei d'Economia de SAP"),
        # self.createObject('Folder', self.context, "Consultoria Ofimàtica"),
        # self.createObject('Folder', self.context, "Contingencia de CMDB Intranet i Kbtic"),
        # self.createObject('Folder', self.context, "Contrasenyes"),
        # self.createObject('Folder', self.context, "Correu electrònic"),
        # self.createObject('Folder', self.context, "Correu Electrònic - Domino"),
        # self.createObject('Folder', self.context, "Correu Electrònic - IIS"),
        # self.createObject('Folder', self.context, "Correu Electrònic - Nous Relays"),
        # self.createObject('Folder', self.context, "Correu Electrònic - PL"),
        # self.createObject('Folder', self.context, "Correu Electrònic - Relay CSPT"),
        # self.createObject('Folder', self.context, "Correu Electrònic - Relays"),
        # self.createObject('Folder', self.context, "Correu Electrònic - SOGo"),
        # self.createObject('Folder', self.context, "Correu Electrònic - Zimbra"),
        # self.createObject('Folder', self.context, "Correu K2"),
        # self.createObject('Folder', self.context, "CostosABC"),
        # self.createObject('Folder', self.context, "CPD"),
        # self.createObject('Folder', self.context, "CSPT"),
        # self.createObject('Folder', self.context, "CTT"),
        # self.createObject('Folder', self.context, "Directori UPC"),
        # self.createObject('Folder', self.context, "Distribució de Software"),
        # self.createObject('Folder', self.context, "DNS"),
        # self.createObject('Folder', self.context, "Documentació"),
        # self.createObject('Folder', self.context, "Documentació de referència"),
        # self.createObject('Folder', self.context, "DOCUMENTUM"),
        # self.createObject('Folder', self.context, "Domini UPCXXI"),
        # self.createObject('Folder', self.context, "Domino"),
        # self.createObject('Folder', self.context, "Dotproject"),
        # self.createObject('Folder', self.context, "Drac"),
        # self.createObject('Folder', self.context, "Drac-UIC"),
        # self.createObject('Folder', self.context, "e-Desk Conferències web"),
        # self.createObject('Folder', self.context, "e-enquestes"),
        # self.createObject('Folder', self.context, "eAdministració"),
        # self.createObject('Folder', self.context, "Enquestes satisfacció ATIC"),
        # self.createObject('Folder', self.context, "Entitat de Registre"),
        # self.createObject('Folder', self.context, "Envío de mensajes vía SMS"),
        # self.createObject('Folder', self.context, "EPI"),
        # self.createObject('Folder', self.context, "Equip de Comunicació"),
        # self.createObject('Folder', self.context, "estadistiques"),
        # self.createObject('Folder', self.context, "Etiquetatge"),
        # self.createObject('Folder', self.context, "ETPL"),
        # self.createObject('Folder', self.context, "Evalwin"),
        # self.createObject('Folder', self.context, "FACIL"),
        # self.createObject('Folder', self.context, "FAMA"),
        # self.createObject('Folder', self.context, "FENIX"),
        # self.createObject('Folder', self.context, "Firewalls"),
        # self.createObject('Folder', self.context, "Fo - Instalacions"),
        # self.createObject('Folder', self.context, "FTP"),
        # self.createObject('Folder', self.context, "Gallery"),
        # self.createObject('Folder', self.context, "GARTNER"),
        # self.createObject('Folder', self.context, "gAUSS"),
        # self.createObject('Folder', self.context, "GCarnet"),
        # self.createObject('Folder', self.context, "gCFG"),
        # self.createObject('Folder', self.context, "gCON"),
        # self.createObject('Folder', self.context, "gCOT"),
        # self.createObject('Folder', self.context, "Generació de Certificats especials"),
        # self.createObject('Folder', self.context, "GenGrups"),
        # self.createObject('Folder', self.context, "GenWeb"),
        # self.createObject('Folder', self.context, "Gestió d'eleccions"),
        # self.createObject('Folder', self.context, "Gestió de garanties"),
        # self.createObject('Folder', self.context, "Gestió Econòmica"),
        # self.createObject('Folder', self.context, "Gestionados"),
        # self.createObject('Folder', self.context, "Gestor de serveis"),
        # self.createObject('Folder', self.context, "GMail"),
        # self.createObject('Folder', self.context, "Google"),
        # self.createObject('Folder', self.context, "Google Apps"),
        # self.createObject('Folder', self.context, "granola"),
        # self.createObject('Folder', self.context, "GRED"),
        # self.createObject('Folder', self.context, "GRED-UNED"),
        # self.createObject('Folder', self.context, "gSMS"),
        # self.createObject('Folder', self.context, "Hosting"),
        # self.createObject('Folder', self.context, "Hosting SBIB"),
        # self.createObject('Folder', self.context, "Hosting Web"),
        # self.createObject('Folder', self.context, "HR-Access"),
        # self.createObject('Folder', self.context, "HTC P3600"),
        # self.createObject('Folder', self.context, "Identitat Digital"),
        # self.createObject('Folder', self.context, "Identity Manager"),
        # self.createObject('Folder', self.context, "IdP UPC"),
        # self.createObject('Folder', self.context, "IMPRESORAS"),
        # self.createObject('Folder', self.context, "Indicadors"),
        # self.createObject('Folder', self.context, "InfoATIC"),
        # self.createObject('Folder', self.context, "Informació de referència"),
        # self.createObject('Folder', self.context, "Informació general"),
        # self.createObject('Folder', self.context, "Infraestructura"),
        # self.createObject('Folder', self.context, "Interlocució"),
        # self.createObject('Folder', self.context, "Intranet"),
        # self.createObject('Folder', self.context, "Intranet UPCnet"),
        # self.createObject('Folder', self.context, "Inventari"),
        # self.createObject('Folder', self.context, "ISO27000"),
        # self.createObject('Folder', self.context, "K2 estudiants"),
        # self.createObject('Folder', self.context, "K2 externs"),
        # self.createObject('Folder', self.context, "K2 UPCnet"),
        # self.createObject('Folder', self.context, "KATA"),
        # self.createObject('Folder', self.context, "LDAP"),
        # self.createObject('Folder', self.context, "LDAP UPC"),
        # self.createObject('Folder', self.context, "LDAP: OpenLdap"),
        # self.createObject('Folder', self.context, "Liceu"),
        # self.createObject('Folder', self.context, "Linux"),
        # self.createObject('Folder', self.context, "Llistes de Distribució"),
        # self.createObject('Folder', self.context, "LOCALES"),
        # self.createObject('Folder', self.context, "LOPD"),
        # self.createObject('Folder', self.context, "LSI"),
        # self.createObject('Folder', self.context, "Mailman"),
        # self.createObject('Folder', self.context, "Majordomo"),
        # self.createObject('Folder', self.context, "Manteniment"),
        # self.createObject('Folder', self.context, "Matricula"),
        # self.createObject('Folder', self.context, "MATUPC"),
        # self.createObject('Folder', self.context, "McAfee"),
        # self.createObject('Folder', self.context, "monCCD"),
        # self.createObject('Folder', self.context, "Monitorització"),
        # self.createObject('Folder', self.context, "Monitorización"),
        # self.createObject('Folder', self.context, "Moodle"),
        # self.createObject('Folder', self.context, "MSDNAA de la UPC"),
        # self.createObject('Folder', self.context, "MSF"),
        # self.createObject('Folder', self.context, "Murzim"),
        # self.createObject('Folder', self.context, "MySQL"),
        # self.createObject('Folder', self.context, "Nagios"),
        # self.createObject('Folder', self.context, "Navision"),
        # self.createObject('Folder', self.context, "Neopolis"),
        # self.createObject('Folder', self.context, "Notes"),
        # self.createObject('Folder', self.context, "NTP"),
        # self.createObject('Folder', self.context, "OAUTH"),
        # self.createObject('Folder', self.context, "OBSOLET"),
        # self.createObject('Folder', self.context, "OEM Cloud Control"),
        # self.createObject('Folder', self.context, "Office"),
        # self.createObject('Folder', self.context, "Oracle"),
        # self.createObject('Folder', self.context, "Pàgines web personals"),
        # self.createObject('Folder', self.context, "Parada total CPD"),
        # self.createObject('Folder', self.context, "Parxeig"),
        # self.createObject('Folder', self.context, "PHP"),
        # self.createObject('Folder', self.context, "Pidgin"),
        # self.createObject('Folder', self.context, "Plafo de Serveis"),
        # self.createObject('Folder', self.context, "PLONE"),
        # self.createObject('Folder', self.context, "POSTGRESQL"),
        # self.createObject('Folder', self.context, "Practicum"),
        # self.createObject('Folder', self.context, "Presència"),
        # self.createObject('Folder', self.context, "Prestecs"),
        # self.createObject('Folder', self.context, "Prisma"),
        # self.createObject('Folder', self.context, "Prisma Renove"),
        # self.createObject('Folder', self.context, "Procediments d'Operació"),
        # self.createObject('Folder', self.context, "Progeny"),
        # self.createObject('Folder', self.context, "Projecte Davyd - Sala Juntes Master's"),
        # self.createObject('Folder', self.context, "Proxy"),
        # self.createObject('Folder', self.context, "Puppet"),
        # self.createObject('Folder', self.context, "Radioenllaços"),
        # self.createObject('Folder', self.context, "RADIUS"),
        # self.createObject('Folder', self.context, "Recuperaciones"),
        # self.createObject('Folder', self.context, "Red Hat"),
        # self.createObject('Folder', self.context, "Redes administradas por UPCnet"),
        # self.createObject('Folder', self.context, "Rem"),
        # self.createObject('Folder', self.context, "Reparacions i Petites Ampliacions de Cablat"),
        # self.createObject('Folder', self.context, "Repositori PL UPCnet"),
        # self.createObject('Folder', self.context, "Repositori UPC"),
        # self.createObject('Folder', self.context, "Resolució d'incidències"),
        # self.createObject('Folder', self.context, "Reus Educat"),
        # self.createObject('Folder', self.context, "Revisat"),
        # self.createObject('Folder', self.context, "Revisió Tiquets"),
        # self.createObject('Folder', self.context, "Revisions Mèdiques"),
        # self.createObject('Folder', self.context, "SAI: Servei d'Accés a Internet"),
        # self.createObject('Folder', self.context, "SAN"),
        # self.createObject('Folder', self.context, "SAP"),
        # self.createObject('Folder', self.context, "SAP Renove"),
        # self.createObject('Folder', self.context, "Seguretat"),
        # self.createObject('Folder', self.context, "Servei de Correcció Òptica d'Exàmens de l'ICE"),
        # self.createObject('Folder', self.context, "Servidor TV per a la UPC"),
        # self.createObject('Folder', self.context, "Servidors"),
        # self.createObject('Folder', self.context, "Servidors llicències"),
        # self.createObject('Folder', self.context, "SIGMA"),
        # self.createObject('Folder', self.context, "SIGVI"),
        # self.createObject('Folder', self.context, "Sirena"),
        # self.createObject('Folder', self.context, "SMS"),
        # self.createObject('Folder', self.context, "SOA"),
        # self.createObject('Folder', self.context, "SPA"),
        # self.createObject('Folder', self.context, "SQLserver"),
        # self.createObject('Folder', self.context, "SSL"),
        # self.createObject('Folder', self.context, "Subministraments"),
        # self.createObject('Folder', self.context, "Subversion"),
        # self.createObject('Folder', self.context, "Suport de 2n nivell"),
        # self.createObject('Folder', self.context, "Suport Tecnic Especialitzat"),
        # self.createObject('Folder', self.context, "Suversion"),
        # self.createObject('Folder', self.context, "Sympa"),
        # self.createObject('Folder', self.context, "Tarifes-Costos Directes"),
        # self.createObject('Folder', self.context, "Tarifes-Simulador de costos"),
        # self.createObject('Folder', self.context, "Tasques Setmanals"),
        # self.createObject('Folder', self.context, "Telefonia"),
        # self.createObject('Folder', self.context, "Telefonia SIP - Contact Center HERMES.NET"),
        # self.createObject('Folder', self.context, "Teletreball"),
        # self.createObject('Folder', self.context, "Televot"),
        # self.createObject('Folder', self.context, "Terminal Server"),
        # self.createObject('Folder', self.context, "TOAD for Oracle"),
        # self.createObject('Folder', self.context, "TOF"),
        # self.createObject('Folder', self.context, "Tomcat"),
        # self.createObject('Folder', self.context, "TOTQ"),
        # self.createObject('Folder', self.context, "Trac"),
        # self.createObject('Folder', self.context, "Traveler"),
        # self.createObject('Folder', self.context, "Tripwire"),
        # self.createObject('Folder', self.context, "Ts"),
        # self.createObject('Folder', self.context, "Ubuntu"),
        # self.createObject('Folder', self.context, "Univers"),
        # self.createObject('Folder', self.context, "Univers.Carnets"),
        # self.createObject('Folder', self.context, "UPCconnect"),
        # self.createObject('Folder', self.context, "UPClink"),
        # self.createObject('Folder', self.context, "videoconferencia"),
        # self.createObject('Folder', self.context, "VPN - UPCNET"),
        # self.createObject('Folder', self.context, "Web treballar.upc.es"),
        # self.createObject('Folder', self.context, "Web UPC"),
        # self.createObject('Folder', self.context, "Web UPCnet"),
        # self.createObject('Folder', self.context, "webDAV - Accés a repositoris de fitxers (UPC/UPCnet) via web"),
        # self.createObject('Folder', self.context, "Web_Edicions"),
        # self.createObject('Folder', self.context, "Web_Factorhuma"),
        # self.createObject('Folder', self.context, "Web_iEMED"),
        # self.createObject('Folder', self.context, "Web_innbox"),
        # self.createObject('Folder', self.context, "Windows"),
        # self.createObject('Folder', self.context, "Windows 7"),
        # self.createObject('Folder', self.context, "Wordpress"),
        # self.createObject('Folder', self.context, "X500"),
        # self.createObject('Folder', self.context, "Xarxa"),
        # self.createObject('Folder', self.context, "Xarxa Troncal"),
        # self.createObject('Folder', self.context, "Xarxes LAN"),
        # self.createObject('Folder', self.context, "XSF"),
        # self.createObject('Folder', self.context, "XSF DIBA"),
        # self.createObject('Folder', self.context, "XSFUPC v2.0"),
        # self.createObject('Folder', self.context, "Z - Informació obsoleta"),
        # self.createObject('Folder', self.context, "Zimbra"),
        # self.createObject('Folder', self.context, "(Not Categorized)"),
        # transaction.commit()
        # import ipdb;ipdb.set_trace()

        session.cookies.update(extra_cookies)
        response = session.post(LOGIN_URL, params, allow_redirects=True)
        cookie = {'Cookie': 'HabCookie=1; Desti=' + URL + '/' + PATH + '; RetornTancar=1; NomUsuari=' + NOTES_USER + ' LtpaToken=' + session.cookies['LtpaToken']}
        response = requests.get(MAIN_URL, headers=cookie)
        #import ipdb;ipdb.set_trace()
        response2 = requests.get(URL + TRAVERSE_PATH + '($All)?OpenView', headers=cookie)
        # Ens quedem ID de la vista
        value = re.search(r'name="ViewUNID"\s+value="(\w+)"', response2.content).groups()[0]

        # url to obtain total entries to import
        toplevelentries = URL + TRAVERSE_PATH + value + '?ReadViewEntries&start=1&count=1'
        startLimit = 1
        xmlLimit = session.get(toplevelentries, headers=cookie)
        limit = re.search(r'toplevelentries="(\w+)"', xmlLimit.content).groups()[0]
        logging.info('Starting Notes Migration process...')
        logging.info('Total objects to import: %s', limit)
        # Uncomment for manual imports...
        startLimit = 2334
        limit = 3500
        logging.info('Total objects importing: %s to %s', startLimit, limit)
        for index in range(startLimit, int(limit) + 1):
            # if index % 40 == 0:  # Wait every pack of imports...
            #     time.sleep(2)
            #     logging.info(' -> 5 seconds pause...')

            path_notes = URL + TRAVERSE_PATH + value + '?ReadViewEntries&start=' + str(index) + '&count=1'
            response3 = session.get(path_notes, headers=cookie)

            # No devuelve los mismos resultados, depende de permisos de usuario.
            # La diferencia está en los docs encriptados de contraseñas
            UID = re.search(r'unid="(\w+)"', response3.content).groups()[0]
            # TODO : Check docs with multiple sections (check if values in 3.1 and 3.2 are well imported)
            final_object = URL + TRAVERSE_PATH + value + '/' + UID + '?OpenDocument&ExpandSection=1,2,3,3.1,3.2,4,5,6,7,8,9,10'
            originNotesObjectUrl = URL + TRAVERSE_PATH + value + '/' + UID
            html = session.get(final_object, headers=cookie)
            htmlContent = str(html.content)  # .encode('iso-8859-1').decode('utf-8')
            try:
                titleObject = re.search(r'name="Subject"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('iso-8859-1').replace("&quot;", '"')
                #titleObject = re.search(r'name="Subject"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"')
            except:
                titleObject = re.search(r'(<title>(.*?)</title>)', htmlContent).groups()[1].decode('iso-8859-1').replace("&quot;", '"')
            if 'Incorrect data type for operator or @Function: Text expected<HR>\n<a href="javascript: onClick=history.back()' in html.content:
                logging.info("ERROR in object %s. NOT MIGRATED! URL: %s", index, originNotesObjectUrl)
            else:
                #htmlContent = str(html.content)  # PRODUCTION
                htmlContent = str(html.content).decode('iso-8859-1').encode('utf-8')  # GOLLUM

                logging.info("#%s# Migrating: %s", index, originNotesObjectUrl)
                logging.info("#%s# Title: %s", index, titleObject)

                creator = re.search(r'name="From"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
                Title = titleObject
                tinyContent = re.search(r'^(.*?)(<script.*/script>)(.*?)(<applet.*/applet)(.*?)(<HEAD.*/HEAD>)(.*?)(.*?)<a\s*href="\/Upcnet\/Backoffice\/manualexp\.nsf\/\(\$All\)\?OpenView">.*$', htmlContent, re.DOTALL | re.MULTILINE).groups()[7]
                object = self.createNotesObject('notesDocument', self.context, Title)
                logging.info("#%s# URL: %s", index, object.absolute_url())
                try:
                    lista = []
                    catServei = re.search(r'name="Serveis"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                    for obj in catServei:
                        #id_cat = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj)[0].id
                        id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id
                        lista = lista + [id_cat]
                        object.setCategory1(lista)
                except:
                    None
                try:
                    lista = []
                    catServeiPPS = re.search(r'name="Productes"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                    for obj in catServeiPPS:
                        #id_cat = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj)[0].id
                        id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id
                        lista = lista + [id_cat]
                        object.setCategory2(lista)
                except:
                    None
                try:
                    # sometimes people write with \ separator, we must force check two options...
                    lista = []
                    categories = re.search(r'name="Categories"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                    for obj in categories:
                        #id_cat = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj)[0].id
                        id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id
                        lista = lista + [id_cat]
                        object.setCategory3(lista)
                except:
                    None
                try:
                    # sometimes people write with \ separator, we must force check two options...
                    lista = []
                    categories = re.search(r'name="Categories"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split('\\')
                    for obj in categories:
                        #id_cat = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj)[0].id
                        id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id

                        lista = lista + [id_cat]
                        object.setCategory3(lista)

                except:
                    None
                object.setTitle(Title)
                object.setCreators(creator)
                object.setExcludeFromNav(True)

                # Import Images of the object
                imatgeSrc = re.findall(r'<img[^>]+src=\"([^\"]+)\"', htmlContent)
                imatgeSrc = [a for a in imatgeSrc if '/Upcnet' in a]
                numimage = 1
                for obj in imatgeSrc:
                    imatge = session.get(URL + obj, headers=cookie)
                    imageObject = self.createNotesObject('Image', object, 'image' + str(numimage))
                    replacedName = (object.absolute_url() + '/image' + str(numimage)).replace('mohinder:8080', 'gw4.beta.upcnet.es')
                    tinyContent = tinyContent.replace(obj, replacedName)
                    logging.info('#%s# Creating image: %s', index, replacedName)
                    numimage = numimage + 1
                    imageObject.setImage(imatge.content)

                # Import Files of the object
                attachSrc = re.findall(r'<a[^>]+href=\"([^\"]+)\"', htmlContent)
                attachSrc = [a for a in attachSrc if '$FILE' in a]
                for obj in attachSrc:
                    try:
                        file = session.get(URL + obj, headers=cookie)
                        filename = obj.split('/')[-1].replace('%20', '_').replace('_', '')
                        normalizedName = getToolByName(self.context, 'plone_utils').normalizeString(filename)
                        # fake the same filename in folder object...
                        contents = object.contentIds()
                        normalizedName = self.calculaNom(contents, normalizedName)
                        fileObject = self.createNotesObject('File', object, normalizedName)
                        replacedName = (object.absolute_url() + '/' + normalizedName).replace('mohinder:8080', 'gw4.beta.upcnet.es')
                        tinyContent = tinyContent.replace(obj, replacedName)
                        logging.info('#%s# Creating file: %s', index, replacedName)
                        fileObject.setFile(file.content)
                        # OpenOffice files internally are saved as ZIP files, we must force metadata...
                        extension = obj.split('.')[-1:][0]
                        if extension == 'odt':
                            fileObject.setFormat('application/vnd.oasis.opendocument.text')
                        if extension == 'ods':
                            fileObject.setFormat('application/vnd.oasis.opendocument.spreadsheet')
                        if extension == 'odp':
                            fileObject.setFormat('application/vnd.oasis.opendocument.presentation')
                        if extension == 'odg':
                            fileObject.setFormat('application/vnd.oasis.opendocument.graphics')
                        if extension == 'doc':
                            fileObject.setFormat('application/msword')
                        if extension == 'docx':
                            fileObject.setFormat('application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                        if extension == 'xls':
                            fileObject.setFormat('application/vnd.ms-excel')
                        if extension == 'xlsx':
                            fileObject.setFormat('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        if extension == 'ppt':
                            fileObject.setFormat('application/vnd.ms-powerpoint')
                        if extension == 'pptx':
                            fileObject.setFormat('application/vnd.openxmlformats-officedocument.presentationml.presentation')                            
                    except:
                        logging.info('#%s# ERROR IMPORTING OBJECT! CHECK IT!', index)
                        pass
                # remove section links...
                removeSections = re.findall(r'(<a[^>]+target="_self">.*?</a>)', tinyContent)
                for obj in removeSections:
                    tinyContent = tinyContent.replace(obj, "")

                # Create modified HTML content with new image/file paths
                object.setBody(tinyContent)
                object.reindexObject()
                transaction.commit()
                # Fix creation Date
                try:
                    Date = re.search(r'name="Date"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('iso-8859-1').replace("&quot;", '"')  # GOLLUM
                    #Date = re.search(r'name="Date"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"')  # PROD
                    if Date == 'Yesterday':
                        import datetime
                        today = datetime.date.today()
                        dateCreatedInNotes = str(today.year) + '-' + str(today.month) + '-' + str(today.day - 1)
                        object.setCreationDate(dateCreatedInNotes)
                    else:
                        dateCreatedInNotes = Date.split('/')[2] + '/' + Date.split('/')[0] + '/' + Date.split('/')[1]
                        object.setCreationDate(dateCreatedInNotes)
                except:
                    pass
                try:
                    Date = re.search(r'name="DateComposed"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('iso-8859-1').replace("&quot;", '"')
                    dateCreatedInNotes = '2012/' + Date.split('/')[1] + '/' + Date.split('/')[0]
                    object.setCreationDate(dateCreatedInNotes)
                except:
                    pass
                # Guardar links a BBDD Notes
                links = re.findall(r'<a[^>]+href=\"([^\"]+)\"', tinyContent)
                f = open('NotesLinksKBTIC.txt', 'a')
                linksNotes = [a for a in links if '?OpenDocument' in a and not 'Section' in a]
                for obj in linksNotes:
                    try:
                        information = '#' + str(index) + '# URL Plone: ' + object.absolute_url() + '\n'
                        f.write(information)
                        information = '#' + str(index) + '## Title Plone: ' + titleObject + '\n'
                        f.write(information)
                        information = '#' + str(index) + '### DocNotes: ' + str(originNotesObjectUrl) + '\n'
                        f.write(information)
                        information = '#' + str(index) + '#### Con links a: ' + str(URL) + str(obj) + '\n'
                        f.write(information)
                    except:
                        pass
                f.close()
                transaction.commit()
                logging.info('#%s# Object migrated correctly.', index)

        logging.info('Done! End of Notes Migration process.')
        return 'OK, imported'

    def calculaNom(self, ids, nom_normalitzat, i=0):
        """
        """

        if i != 0:
            nom = nom_normalitzat + str(i)
        else:
            nom = nom_normalitzat

        if nom not in ids:
            return nom
        else:
            return self.calculaNom(ids, nom_normalitzat, i + 1)

    def createNotesObject(self, type, folder, title):
        """
        """
        id = self.generateUnusedId(title)
        _createObjectByType(type, folder, id)
        obj = folder[id]

        return obj

    def generateUnusedId(self, title):
        """
        """
        plone_utils = getToolByName(self.context, 'plone_utils')
        id = plone_utils.normalizeString(title)
        if id in self.context.contentIds():
            number = 2
            while '%s-%i' % (id, number) in self.context.contentIds():
                number += 1
            id = '%s-%i' % (id, number)
        return id

    def createObject(self, type, folder, title):
        """
        """
        id = self.generateUnusedId(title)
        _createObjectByType(type, folder, id=id, title=title)
        obj = folder[id]

        return obj


### EOF ###
