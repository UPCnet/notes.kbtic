# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from plone.app.controlpanel.mail import IMailSchema
from Products.CMFPlone.utils import normalizeString


def setupVarious(context):
    if context.readDataFile('notes.kbtic_various.txt') is None:
        return
    portal = context.getSite()

    # permetre @. als usernames
    portal.portal_registration.manage_editIDPattern('^[A-Za-z][A-Za-z0-9_\-@.]*$')

    # configurem mail
    mail = IMailSchema(portal)
    mail.smtp_host = u'localhost'
    mail.email_from_name = "Administrador Web"
    mail.email_from_address = "noreply@localhost.cat"

    # Paraules clau Serveis
    voctool = getToolByName(portal, 'portal_vocabularies')
    try:
        category1_keywords = _createObjectByType('SortedSimpleVocabulary', voctool, 'category1_keywords')
        keywords = [
                    (u"catServei-01", u"Actualització de continguts en el Web UPC"),
                    (u"catServei-02", u"ACUP - Doc6"),
                    (u"catServei-03", u"Address Book - PAB"),
                    (u"catServei-04", u"Adminpack"),
                    (u"catServei-05", u"Adquira"),
                    (u"catServei-06", u"Alumni UPC"),
                    (u"catServei-07", u"Antivirus"),
                    (u"catServei-08", u"ARI"),
                    (u"catServei-09", u"Atenció Immediata"),
                    (u"catServei-10", u"Atenció Usuaris"),
                    (u"catServei-11", u"Backups"),
                    (u"catServei-12", u"Bases de dades bibliogràfiques"),
                    (u"catServei-13", u"Bibliotècnica"),
                    (u"catServei-14", u"Blackberry Enterprise Server"),
                    (u"catServei-15", u"Campus Digital"),
                    (u"catServei-16", u"Campus Digital - Atenea Mobil"),
                    (u"catServei-17", u"Campus Digital - Atenea1x1"),
                    (u"catServei-18", u"Campus Digital - AteneaSaurus"),
                    (u"catServei-19", u"Campus Digital - Externs"),
                    (u"catServei-20", u"Campus Digital - Moodle"),
                    (u"catServei-21", u"Canal UPC TV"),
                    (u"catServei-22", u"Canvis de contrasenya"),
                    (u"catServei-23", u"Carnet UPC"),
                    (u"catServei-24", u"CAS - Central authentication service"),
                    (u"catServei-25", u"Catàleg de les biblioteques de la UPC"),
                    (u"catServei-26", u"CCE"),
                    (u"catServei-27", u"Cerca d'adreces de correu en webs vulnerables a l'spam"),
                    (u"catServei-28", u"Cercador UPC"),
                    (u"catServei-29", u"Certificats"),
                    (u"catServei-30", u"Clients Externs UPCnet"),
                    (u"catServei-31", u"Cloud privat upc"),
                    (u"catServei-32", u"CMSW"),
                    (u"catServei-33", u"Col·laboratoris"),
                    (u"catServei-34", u"Connexió Remota VNC"),
                    (u"catServei-35", u"Correu Electrònic"),
                    (u"catServei-36", u"Correu Electrònic - Domino"),
                    (u"catServei-37", u"Correu Electrònic - Nous Relays"),
                    (u"catServei-38", u"Correu Electrònic - PL"),
                    (u"catServei-39", u"Correu Electrònic - Relays"),
                    (u"catServei-40", u"CSPT"),
                    (u"catServei-41", u"Directori UPC"),
                    (u"catServei-42", u"Distribucio de Software"),
                    (u"catServei-43", u"DNS"),
                    (u"catServei-44", u"DOCUMENTUM"),
                    (u"catServei-45", u"Domini UPCXXI"),
                    (u"catServei-46", u"Domino"),
                    (u"catServei-47", u"Drac"),
                    (u"catServei-48", u"e-Desk Conferències web"),
                    (u"catServei-49", u"e-enquestes"),
                    (u"catServei-50", u"eAdministració"),
                    (u"catServei-51", u"Entitat de Registre"),
                    (u"catServei-52", u"Envío de mensajes vía SMS"),
                    (u"catServei-53", u"EPI"),
                    (u"catServei-54", u"etpl"),
                    (u"catServei-55", u"Evalwin"),
                    (u"catServei-56", u"FACIL"),
                    (u"catServei-57", u"FAMA"),
                    (u"catServei-58", u"FENIX"),
                    (u"catServei-59", u"Firewalls"),
                    (u"catServei-60", u"Gartner"),
                    (u"catServei-61", u"gAUSS"),
                    (u"catServei-62", u"gCFG"),
                    (u"catServei-63", u"gCON"),
                    (u"catServei-64", u"gCOT"),
                    (u"catServei-65", u"Generació de certificats especials"),
                    (u"catServei-66", u"GenGrups"),
                    (u"catServei-67", u"GenWeb"),
                    (u"catServei-68", u"Gestió d'eleccions"),
                    (u"catServei-69", u"Gestió de garanties"),
                    (u"catServei-70", u"Gestionados"),
                    (u"catServei-71", u"Gestor de serveis"),
                    (u"catServei-72", u"GRED"),
                    (u"catServei-73", u"GRED-UNED"),
                    (u"catServei-74", u"gSMS"),
                    (u"catServei-75", u"Hosting"),
                    (u"catServei-76", u"Hosting Web"),
                    (u"catServei-77", u"HR-Access"),
                    (u"catServei-78", u"Identitat Digital"),
                    (u"catServei-79", u"IdP UPC"),
                    (u"catServei-80", u"Intranet"),
                    (u"catServei-81", u"Intranet UPCnet"),
                    (u"catServei-82", u"K2 estudiants"),
                    (u"catServei-83", u"K2 externs"),
                    (u"catServei-84", u"K2 UPCnet"),
                    (u"catServei-85", u"KATA"),
                    (u"catServei-86", u"LDAP"),
                    (u"catServei-87", u"LDAP UPC"),
                    (u"catServei-88", u"LDAP: OpenLdap"),
                    (u"catServei-89", u"Liceu"),
                    (u"catServei-90", u"Linux"),
                    (u"catServei-91", u"Majordomo"),
                    (u"catServei-92", u"Manteniment"),
                    (u"catServei-93", u"Matricula"),
                    (u"catServei-94", u"MATUPC"),
                    (u"catServei-95", u"monCCD"),
                    (u"catServei-96", u"Monitorització"),
                    (u"catServei-97", u"Monitorización"),
                    (u"catServei-98", u"Mysql"),
                    (u"catServei-99", u"Navision"),
                    (u"catServei-100", u"Notes"),
                    (u"catServei-101", u"OBSOLET"),
                    (u"catServei-102", u"Pàgines web personals"),
                    (u"catServei-103", u"Pidgin"),
                    (u"catServei-104", u"PLONE"),
                    (u"catServei-105", u"Practicum"),
                    (u"catServei-106", u"Presencia"),
                    (u"catServei-107", u"Prisma"),
                    (u"catServei-108", u"Prisma Renove"),
                    (u"catServei-109", u"Progeny"),
                    (u"catServei-110", u"Projecte Davyd - Sala Juntes Master's"),
                    (u"catServei-111", u"Proxy"),
                    (u"catServei-112", u"Redes administradas por UPCnet"),
                    (u"catServei-113", u"Reparacions i Petites Ampliacions de Cablat"),
                    (u"catServei-114", u"Repositori PL UPCnet"),
                    (u"catServei-115", u"Resolució d'incidències"),
                    (u"catServei-116", u"Reus Educat"),
                    (u"catServei-117", u"Revisat"),
                    (u"catServei-118", u"Revisions Mèdiques"),
                    (u"catServei-119", u"SAI: Servei d'Accés a Internet"),
                    (u"catServei-120", u"SAP"),
                    (u"catServei-121", u"Seguretat"),
                    (u"catServei-122", u"Servei de Correcció Òptica d'Exàmens de l'ICE"),
                    (u"catServei-123", u"Servidor TV per a la UPC"),
                    (u"catServei-124", u"Servidors"),
                    (u"catServei-125", u"SIGMA"),
                    (u"catServei-126", u"SIrena"),
                    (u"catServei-127", u"Spa"),
                    (u"catServei-128", u"SQLserver"),
                    (u"catServei-129", u"SSL"),
                    (u"catServei-130", u"Suport de 2n nivell"),
                    (u"catServei-131", u"Suport Tecnic Especialitzat"),
                    (u"catServei-132", u"Sympa"),
                    (u"catServei-133", u"Tarifes-Costos Directes"),
                    (u"catServei-134", u"Tarifes-Simulador de costos"),
                    (u"catServei-135", u"Telefonia"),
                    (u"catServei-136", u"Teletreball"),
                    (u"catServei-137", u"Televot"),
                    (u"catServei-138", u"TOF"),
                    (u"catServei-139", u"TOTQ"),
                    (u"catServei-140", u"Traveler"),
                    (u"catServei-141", u"Ts"),
                    (u"catServei-142", u"Ubuntu"),
                    (u"catServei-143", u"UPCconnect"),
                    (u"catServei-144", u"UPClink"),
                    (u"catServei-145", u"videoconferencia"),
                    (u"catServei-146", u"Web UPC"),
                    (u"catServei-147", u"Web UPCnet"),
                    (u"catServei-148", u"webDAV - Accés a repositoris de fitxers (UPC/UPCnet) via web"),
                    (u"catServei-149", u"Web_Edicions"),
                    (u"catServei-150", u"Xarxa"),
                    (u"catServei-151", u"Xarxa Troncal"),
                    (u"catServei-152", u"XSF"),
                    (u"catServei-153", u"XSF DIBA"),
                    (u"catServei-154", u"Z - Informació obsoleta"),
                     ]
        for keyword in keywords:
            object = _createObjectByType('SimpleVocabularyTerm', category1_keywords, keyword[0])
            object.setTitle(keyword[1])
            object.reindexObject()
    except:
        pass

    #paraules clau Servei PPS
    try:
        category2_keywords = _createObjectByType('SortedSimpleVocabulary', voctool, 'category2_keywords')
        keywords = [
                    (u"catServeiPPS-01", u"gSMS - Gestió d'enviament d'SMS"),
                    (u"catServeiPPS-02", u"10100-00 Atenció a  l'usuari"),
                    (u"catServeiPPS-03", u"10101-00 Correcció exàmens ICE"),
                    (u"catServeiPPS-04", u"10200-00 Resolució de consultes ofimàtiques"),
                    (u"catServeiPPS-05", u"10300-00 Correu electrònic"),
                    (u"catServeiPPS-06", u"10301-00 Correu electrònic DN"),
                    (u"catServeiPPS-07", u"10302-00 Correu electrònic K2"),
                    (u"catServeiPPS-08", u"10303-00 Relay i gestió de dominis de correu"),
                    (u"catServeiPPS-09", u"10304-00 Llistes de distribució de correu"),
                    (u"catServeiPPS-10", u"10312-00 Agenda K2"),
                    (u"catServeiPPS-11", u"10350-00 Missatgeria instantània"),
                    (u"catServeiPPS-12", u"10400-00 Impressió en xarxa"),
                    (u"catServeiPPS-13", u"10500-00 Repositori de fitxers"),
                    (u"catServeiPPS-14", u"10501-00 Repositori de fitxers personals"),
                    (u"catServeiPPS-15", u"10502-00 Repositori de fitxers de grup"),
                    (u"catServeiPPS-16", u"10600-00 Gestió d'estacions de treball personals"),
                    (u"catServeiPPS-17", u"10610-00 Configuració mantinguda de software"),
                    (u"catServeiPPS-18", u"10611-00 Configuració mantinguda de software - entorn Windows"),
                    (u"catServeiPPS-19", u"10612-00 Configuració mantinguda de software - entorn Linux"),
                    (u"catServeiPPS-20", u"10612-01 Configuració PUB-Linux (SBD)"),
                    (u"catServeiPPS-21", u"10620-00 Instal·lació de software"),
                    (u"catServeiPPS-22", u"10800-00 Xarxa sense fils (XSF)"),
                    (u"catServeiPPS-23", u"10900-00 Dispositius mòbils"),
                    (u"catServeiPPS-24", u"10910-00 Blackberry DN"),
                    (u"catServeiPPS-25", u"11000-00 Bases de dades bibliogràfiques en CD-ROM"),
                    (u"catServeiPPS-26", u"11100-00 Hosting de pàgines web personals"),
                    (u"catServeiPPS-27", u"12100-00 Suport tècnic especialitzat"),
                    (u"catServeiPPS-28", u"12110-00 Assessorament a PAS TIC de la UPC"),
                    (u"catServeiPPS-29", u"12110-00 Suport de 2n nivell"),
                    (u"catServeiPPS-30", u"14000-00 Portal de serveis a l'usuari"),
                    (u"catServeiPPS-31", u"20100-00 Subministraments"),
                    (u"catServeiPPS-32", u"20104-00 Subministrament d'equips de telefonia fixa"),
                    (u"catServeiPPS-33", u"20108-00 Adquisició de llicències de software"),
                    (u"catServeiPPS-34", u"20200-00 Manteniment"),
                    (u"catServeiPPS-35", u"20201-00 Manteniment de llicències de software base de servidors"),
                    (u"catServeiPPS-36", u"20206-00 Manteniment hardware d'equips ofimàtics"),
                    (u"catServeiPPS-37", u"20207-00 Manteniment hardware d'equips electrònics de comunicacions de dades"),
                    (u"catServeiPPS-38", u"20208-00 Manteniment hardware de servidors"),
                    (u"catServeiPPS-39", u"20300-00 Telefonia mòbil"),
                    (u"catServeiPPS-40", u"20304-00 gSMS - Gestió d'enviament d'SMS"),
                    (u"catServeiPPS-41", u"20400-00 Distribució de software"),
                    (u"catServeiPPS-42", u"20401-00 Distribució de llicències de software i control de llicències flotants"),
                    (u"catServeiPPS-43", u"20500-00 Gestió de garanties"),
                    (u"catServeiPPS-44", u"20600-00 KATA: portal de compres TIC"),
                    (u"catServeiPPS-45", u"30100-00 Directori / Intranet"),
                    (u"catServeiPPS-46", u"30101-00 Directori"),
                    (u"catServeiPPS-47", u"30102-00 Identificació a la Intranet"),
                    (u"catServeiPPS-48", u"30103-00 Autenticació Directori LDAP"),
                    (u"catServeiPPS-49", u"30104-00 gAUSS - gestió de l'Autenticació d'USuaris i Serveis"),
                    (u"catServeiPPS-50", u"30104-00 gAUSS - gestió de la Autenticació d'USuaris i Serveis"),
                    (u"catServeiPPS-51", u"30110-00"),
                    (u"catServeiPPS-52", u"30110-00 Certificació Carnet UPC"),
                    (u"catServeiPPS-53", u"30200-00 Campus Digitals i col·laboratoris per a la docència"),
                    (u"catServeiPPS-54", u"30300-00 Gestió econòmica"),
                    (u"catServeiPPS-55", u"30400-00 Gestió de personal"),
                    (u"catServeiPPS-56", u"30500-00 Petits ERP"),
                    (u"catServeiPPS-57", u"30501-00 gRED - Gestió del registre d'entrada i sortida de documents"),
                    (u"catServeiPPS-58", u"30503-00 Gestió de relacions institucionals i internacionals"),
                    (u"catServeiPPS-59", u"30504-00 gCOT - Gestió de Consums de Telefonia"),
                    (u"catServeiPPS-60", u"30600-00 Gestió de la docència"),
                    (u"catServeiPPS-61", u"30600-00 Gestió de la docència i la recerca"),
                    (u"catServeiPPS-62", u"30610-00 Gestió de la matriculació de primer i segon cicle"),
                    (u"catServeiPPS-63", u"30612-00 Gestió de titulacions"),
                    (u"catServeiPPS-64", u"30613-00 Gestió del doctorat"),
                    (u"catServeiPPS-65", u"30640-00 Gestió de l'Associació d'Amics de la UPC"),
                    (u"catServeiPPS-66", u"30800-00 Gestió de biblioteques"),
                    (u"catServeiPPS-67", u"39000-00 Gestió de les enquestes de professors"),
                    (u"catServeiPPS-68", u"40100-00 Sistemes d'Informació d'UPCnet"),
                    (u"catServeiPPS-69", u"40102-00 Gestió de l'atenció a l'usuari (ATIC)"),
                    (u"catServeiPPS-70", u"40102-00 Gestor de Serveis"),
                    (u"catServeiPPS-71", u"40104-00 Intranet d'UPCnet"),
                    (u"catServeiPPS-72", u"40200-00 Allotjament de webs i col·laboratoris"),
                    (u"catServeiPPS-73", u"40200-00 Hosting de col·laboratoris"),
                    (u"catServeiPPS-74", u"40201-00 Allotjament de webs i col·laboratoris sobre Linux"),
                    (u"catServeiPPS-75", u"40202-00 Allotjament de webs i col·laboratoris sobre Lotus Domino"),
                    (u"catServeiPPS-76", u"40202-01 Allotjament de Web i Col·laboratoris en tecnologia Lotus Domino - Família"),
                    (u"catServeiPPS-77", u"40204-00 Allotjament de Web i Col·laboratoris al domini www.upc.edu"),
                    (u"catServeiPPS-78", u"40204-00 Web corporativa de la UPC"),
                    (u"catServeiPPS-79", u"40300-00 Sistemes de gestió de continguts web"),
                    (u"catServeiPPS-80", u"40301-00 Eines de gestió de Web i Col·laboratoris basats en Plone"),
                    (u"catServeiPPS-81", u"40301-00 GenWeb UPC"),
                    (u"catServeiPPS-82", u"50102-00 Instal·lació de software base de servidors"),
                    (u"catServeiPPS-83", u"50111-00 Hosting de servidors"),
                    (u"catServeiPPS-84", u"50111-00 Hosting dedicat de servidors"),
                    (u"catServeiPPS-85", u"50113-00 Hosting d'aplicacions"),
                    (u"catServeiPPS-86", u"50121-00 Hosting compartit i  webs"),
                    (u"catServeiPPS-87", u"50121-00 Hosting de webs"),
                    (u"catServeiPPS-88", u"50122-00 Allotjament i administració de webs"),
                    (u"catServeiPPS-89", u"50123-00 Hosting compartit de BBDD"),
                    (u"catServeiPPS-90", u"50124-00 Hosting Prisma"),
                    (u"catServeiPPS-91", u"50201-00 Monitorització de servidors"),
                    (u"catServeiPPS-92", u"50202-00 Còpies de seguretat de dades de servidors no gestionats per UPCnet"),
                    (u"catServeiPPS-93", u"50301-00 Gestió de dominis d'Internet (DNS)"),
                    (u"catServeiPPS-94", u"50403-00 Telefonia fixa"),
                    (u"catServeiPPS-95", u"50404-00 Telefonia fixa IP"),
                    (u"catServeiPPS-96", u"50501-00 Instal·lació d'equips electrònics de comunicacions de dades"),
                    (u"catServeiPPS-97", u"50502-00 Instal·lació de punts de xarxa"),
                    (u"catServeiPPS-98", u"50503-00 Manteniment del cablat de xarxa"),
                    (u"catServeiPPS-99", u"50504-00 Administració de xarxes locals"),
                    (u"catServeiPPS-100", u"50504-00 Administració i connexió de xarxes locals"),
                    (u"catServeiPPS-101", u"50505-00 Reparacions i petites ampliacions de cablat"),
                    (u"catServeiPPS-102", u"50551-00 Administració de la xarxa troncal i la connexió a Internet"),
                    (u"catServeiPPS-103", u"50601-00 Accés remot als recursos informàtics de la UPC i a Internet"),
                    (u"catServeiPPS-104", u"50602-00 Accés remot a Internet"),
                    (u"catServeiPPS-105", u"50602-00 Accés remot a Internet (accés ""UPCnet"")"),
                    (u"catServeiPPS-106", u"50604-00 Accés remot a Internet (antic accés UPCnet)"),
                    (u"catServeiPPS-107", u"50801-00 Tallafocs de Campus gestionats"),
                    (u"catServeiPPS-108", u"50802-00 Tallafocs Externs gestionats"),
                    (u"catServeiPPS-109", u"50900-00 Xarxa Sense Fils (XSF)"),
                    (u"catServeiPPS-110", u"60101-00 Adaptació ergonòmica i de la usabilitat d’aplicatius"),
                    (u"catServeiPPS-111", u"60102-00 Assessoria i consultoria en disseny"),
                    (u"catServeiPPS-112", u"60105-00 Creació de Programes d’imatge corporativa"),
                    (u"catServeiPPS-113", u"60200-00 reus eduCAT"),
                    (u"catServeiPPS-114", u"70000-00 Assessorament general sobre les TIC"),
                    (u"catServeiPPS-115", u"80000-00 Altres productes"),
                    (u"catServeiPPS-116", u"80100-00 Genèric (global a varis productes)"),
                    (u"catServeiPPS-117", u"90000-00 Sense Servei"),
                    (u"catServeiPPS-118", u"Directiva organizativa: %s|(No se ha asignado ninguna directiva explícita)|(No  se"),
                    (u"catServeiPPS-119", u"(Not Categorized)"),
                       ]
        for keyword in keywords:
            object = _createObjectByType('SimpleVocabularyTerm', category2_keywords, keyword[0])
            object.setTitle(keyword[1])
            object.reindexObject()
    except:
        pass

    #paraules clau By Category
    try:
        category3_keywords = _createObjectByType('SortedSimpleVocabulary', voctool, 'category3_keywords')
        keywords = [
                    (u"categoria-1", u"0 - CONTENIDO DE ESTA BD"),
                    (u"categoria-2", u"01 - UTILIDADES"),
                    (u"categoria-3", u"Active Directory"),
                    (u"categoria-4", u"Actualització de continguts en el Web UPC"),
                    (u"categoria-5", u"ACUP - Doc6"),
                    (u"categoria-6", u"Address Book - PAB"),
                    (u"categoria-7", u"Adminpack"),
                    (u"categoria-8", u"Adquira"),
                    (u"categoria-9", u"Altes Estudiants"),
                    (u"categoria-10", u"Alumni UPC"),
                    (u"categoria-11", u"Amics"),
                    (u"categoria-12", u"Antivirus"),
                    (u"categoria-13", u"Aparador"),
                    (u"categoria-14", u"APS"),
                    (u"categoria-15", u"ARA"),
                    (u"categoria-16", u"Archibus"),
                    (u"categoria-17", u"ARI"),
                    (u"categoria-18", u"Atenció Immediata"),
                    (u"categoria-19", u"Atenció telefònica Centraleta UPCnet"),
                    (u"categoria-20", u"Atenció Usuaris"),
                    (u"categoria-21", u"Atenea"),
                    (u"categoria-22", u"Backoffice"),
                    (u"categoria-23", u"Backups"),
                    (u"categoria-24", u"Bases de dades bibliogràfiques"),
                    (u"categoria-25", u"Bi"),
                    (u"categoria-26", u"Bibliotècnica"),
                    (u"categoria-27", u"Bizagi"),
                    (u"categoria-28", u"Blackberry Enterprise Server"),
                    (u"categoria-29", u"Boyce"),
                    (u"categoria-30", u"Cacti"),
                    (u"categoria-31", u"Campus Digital"),
                    (u"categoria-32", u"Campus Digital - Atenea Mobil"),
                    (u"categoria-33", u"Campus Digital - Atenea1x1"),
                    (u"categoria-34", u"Campus Digital - AteneaSaurus"),
                    (u"categoria-35", u"Campus Digital - Externs"),
                    (u"categoria-36", u"Campus Digital - Moodle"),
                    (u"categoria-37", u"Campus Digital - OFA/SDP"),
                    (u"categoria-38", u"Canal UPC TV"),
                    (u"categoria-39", u"Canvis de contrasenya"),
                    (u"categoria-40", u"Carnet UPC"),
                    (u"categoria-41", u"Carrega Estudiants al PAB EST-UPC"),
                    (u"categoria-42", u"CAS - Central authentication service"),
                    (u"categoria-43", u"Catàleg de les biblioteques de la UPC"),
                    (u"categoria-44", u"CBL"),
                    (u"categoria-45", u"CCE"),
                    (u"categoria-46", u"Cerca d'adreces de correu en webs vulnerables a l'spam"),
                    (u"categoria-47", u"Cercador UPC"),
                    (u"categoria-48", u"Certificat digital"),
                    (u"categoria-49", u"Certificats"),
                    (u"categoria-50", u"Certificats arrels webs UPC / UPCnet"),
                    (u"categoria-51", u"Circinus"),
                    (u"categoria-52", u"Clients Externs UPCnet"),
                    (u"categoria-53", u"CLOUD Privat UPC"),
                    (u"categoria-54", u"Cluster DN"),
                    (u"categoria-55", u"CMSW"),
                    (u"categoria-56", u"Col·laboratoris"),
                    (u"categoria-57", u"Connexió Remota VNC"),
                    (u"categoria-58", u"Consoles"),
                    (u"categoria-59", u"Consulta web administradors del Servei d'Economia de SAP"),
                    (u"categoria-60", u"Consultoria Ofimàtica"),
                    (u"categoria-61", u"Contingencia de CMDB Intranet i Kbtic"),
                    (u"categoria-62", u"Contrasenyes"),
                    (u"categoria-63", u"Correu electrònic"),
                    (u"categoria-64", u"Correu Electrònic - Domino"),
                    (u"categoria-65", u"Correu Electrònic - IIS"),
                    (u"categoria-66", u"Correu Electrònic - Nous Relays"),
                    (u"categoria-67", u"Correu Electrònic - PL"),
                    (u"categoria-68", u"Correu Electrònic - Relay CSPT"),
                    (u"categoria-69", u"Correu Electrònic - Relays"),
                    (u"categoria-70", u"Correu Electrònic - SOGo"),
                    (u"categoria-71", u"Correu Electrònic - Zimbra"),
                    (u"categoria-72", u"Correu K2"),
                    (u"categoria-73", u"CostosABC"),
                    (u"categoria-74", u"CPD"),
                    (u"categoria-75", u"CSPT"),
                    (u"categoria-76", u"CTT"),
                    (u"categoria-77", u"Directori UPC"),
                    (u"categoria-78", u"Distribució de Software"),
                    (u"categoria-79", u"DNS"),
                    (u"categoria-80", u"Documentació"),
                    (u"categoria-81", u"Documentació de referència"),
                    (u"categoria-82", u"DOCUMENTUM"),
                    (u"categoria-83", u"Domini UPCXXI"),
                    (u"categoria-84", u"Domino"),
                    (u"categoria-85", u"Dotproject"),
                    (u"categoria-86", u"Drac"),
                    (u"categoria-87", u"Drac-UIC"),
                    (u"categoria-88", u"e-Desk Conferències web"),
                    (u"categoria-89", u"e-enquestes"),
                    (u"categoria-90", u"eAdministració"),
                    (u"categoria-91", u"Enquestes satisfacció ATIC"),
                    (u"categoria-92", u"Entitat de Registre"),
                    (u"categoria-93", u"Envío de mensajes vía SMS"),
                    (u"categoria-94", u"EPI"),
                    (u"categoria-95", u"Equip de Comunicació"),
                    (u"categoria-96", u"ESRI"),
                    (u"categoria-97", u"estadistiques"),
                    (u"categoria-98", u"Etiquetatge"),
                    (u"categoria-99", u"ETPL"),
                    (u"categoria-100", u"Evalwin"),
                    (u"categoria-101", u"FACIL"),
                    (u"categoria-102", u"FAMA"),
                    (u"categoria-103", u"FENIX"),
                    (u"categoria-104", u"Firewalls"),
                    (u"categoria-105", u"Fo - Instalacions"),
                    (u"categoria-106", u"FTP"),
                    (u"categoria-107", u"Gallery"),
                    (u"categoria-108", u"GARTNER"),
                    (u"categoria-109", u"gAUSS"),
                    (u"categoria-110", u"GCarnet"),
                    (u"categoria-111", u"gCFG"),
                    (u"categoria-112", u"gCON"),
                    (u"categoria-113", u"gCOT"),
                    (u"categoria-114", u"Generació de Certificats especials"),
                    (u"categoria-115", u"GenGrups"),
                    (u"categoria-116", u"GenWeb"),
                    (u"categoria-117", u"Gestió d'eleccions"),
                    (u"categoria-118", u"Gestió de garanties"),
                    (u"categoria-119", u"Gestió Econòmica"),
                    (u"categoria-120", u"Gestionados"),
                    (u"categoria-121", u"Gestor de serveis"),
                    (u"categoria-122", u"GMail"),
                    (u"categoria-123", u"Google"),
                    (u"categoria-124", u"Google Apps"),
                    (u"categoria-125", u"granola"),
                    (u"categoria-126", u"GRED"),
                    (u"categoria-127", u"GRED-UNED"),
                    (u"categoria-128", u"gSMS"),
                    (u"categoria-129", u"Hosting"),
                    (u"categoria-130", u"Hosting SBIB"),
                    (u"categoria-131", u"Hosting Web"),
                    (u"categoria-132", u"HR-Access"),
                    (u"categoria-133", u"HTC P3600"),
                    (u"categoria-134", u"Identitat Digital"),
                    (u"categoria-135", u"Identity Manager"),
                    (u"categoria-136", u"IdP UPC"),
                    (u"categoria-137", u"IMPRESORAS"),
                    (u"categoria-138", u"Indicadors"),
                    (u"categoria-139", u"InfoATIC"),
                    (u"categoria-140", u"Informació de referència"),
                    (u"categoria-141", u"Informació general"),
                    (u"categoria-142", u"Infraestructura"),
                    (u"categoria-143", u"Interlocució"),
                    (u"categoria-144", u"Intranet"),
                    (u"categoria-145", u"Intranet UPCnet"),
                    (u"categoria-146", u"Inventari"),
                    (u"categoria-147", u"ISO27100"),
                    (u"categoria-148", u"K2 estudiants"),
                    (u"categoria-149", u"K2 externs"),
                    (u"categoria-150", u"K2 UPCnet"),
                    (u"categoria-151", u"KATA"),
                    (u"categoria-152", u"LDAP"),
                    (u"categoria-153", u"LDAP UPC"),
                    (u"categoria-154", u"LDAP: OpenLdap"),
                    (u"categoria-155", u"Liceu"),
                    (u"categoria-156", u"Linux"),
                    (u"categoria-157", u"Llicencies"),
                    (u"categoria-158", u"Llistes de Distribució"),
                    (u"categoria-159", u"LOCALES"),
                    (u"categoria-160", u"LOPD"),
                    (u"categoria-161", u"LSI"),
                    (u"categoria-162", u"Mailman"),
                    (u"categoria-163", u"Majordomo"),
                    (u"categoria-164", u"Manteniment"),
                    (u"categoria-165", u"Matricula"),
                    (u"categoria-166", u"MATUPC"),
                    (u"categoria-167", u"McAfee"),
                    (u"categoria-168", u"monCCD"),
                    (u"categoria-169", u"Monitorització"),
                    (u"categoria-170", u"Monitorización"),
                    (u"categoria-171", u"Moodle"),
                    (u"categoria-172", u"MSDNAA de la UPC"),
                    (u"categoria-173", u"MSF"),
                    (u"categoria-174", u"Murzim"),
                    (u"categoria-175", u"MySQL"),
                    (u"categoria-176", u"Nagios"),
                    (u"categoria-177", u"Navision"),
                    (u"categoria-178", u"Neopolis"),
                    (u"categoria-179", u"Notes"),
                    (u"categoria-180", u"NTP"),
                    (u"categoria-181", u"OAUTH"),
                    (u"categoria-182", u"OBSOLET"),
                    (u"categoria-183", u"OEM Cloud Control"),
                    (u"categoria-184", u"Office"),
                    (u"categoria-185", u"Oracle"),
                    (u"categoria-186", u"Pàgines web personals"),
                    (u"categoria-187", u"Parada total CPD"),
                    (u"categoria-188", u"Parxeig"),
                    (u"categoria-189", u"PHP"),
                    (u"categoria-190", u"Pidgin"),
                    (u"categoria-191", u"Plafo de Serveis"),
                    (u"categoria-192", u"PLONE"),
                    (u"categoria-193", u"POSTGRESQL"),
                    (u"categoria-194", u"Practicum"),
                    (u"categoria-195", u"Presència"),
                    (u"categoria-196", u"Prestecs"),
                    (u"categoria-197", u"Prisma"),
                    (u"categoria-198", u"Prisma Renove"),
                    (u"categoria-199", u"Procediments d'Operació"),
                    (u"categoria-200", u"Progeny"),
                    (u"categoria-201", u"Projecte Davyd - Sala Juntes Master's"),
                    (u"categoria-202", u"Proxy"),
                    (u"categoria-203", u"Puppet"),
                    (u"categoria-204", u"Radioenllaços"),
                    (u"categoria-205", u"RADIUS"),
                    (u"categoria-206", u"Recuperaciones"),
                    (u"categoria-207", u"Red Hat"),
                    (u"categoria-208", u"Redes administradas por UPCnet"),
                    (u"categoria-209", u"Rem"),
                    (u"categoria-210", u"Reparacions i Petites Ampliacions de Cablat"),
                    (u"categoria-211", u"Repositori PL UPCnet"),
                    (u"categoria-212", u"Repositori UPC"),
                    (u"categoria-213", u"Resolució d'incidències"),
                    (u"categoria-214", u"Reus Educat"),
                    (u"categoria-215", u"Revisat"),
                    (u"categoria-216", u"Revisió Tiquets"),
                    (u"categoria-217", u"Revisions Mèdiques"),
                    (u"categoria-218", u"SAI: Servei d'Accés a Internet"),
                    (u"categoria-219", u"SAN"),
                    (u"categoria-220", u"SAP"),
                    (u"categoria-221", u"SAP Renove"),
                    (u"categoria-222", u"Seguretat"),
                    (u"categoria-223", u"Servei de Correcció Òptica d'Exàmens de l'ICE"),
                    (u"categoria-224", u"Servidor TV per a la UPC"),
                    (u"categoria-225", u"Servidors"),
                    (u"categoria-226", u"Servidors llicències"),
                    (u"categoria-227", u"SIGMA"),
                    (u"categoria-228", u"SIGVI"),
                    (u"categoria-229", u"Sirena"),
                    (u"categoria-230", u"SMS"),
                    (u"categoria-231", u"SOA"),
                    (u"categoria-232", u"SPA"),
                    (u"categoria-233", u"SQLserver"),
                    (u"categoria-234", u"SSL"),
                    (u"categoria-235", u"Subministraments"),
                    (u"categoria-236", u"Subversion"),
                    (u"categoria-237", u"Suport de 2n nivell"),
                    (u"categoria-238", u"Suport Tecnic Especialitzat"),
                    (u"categoria-239", u"Suversion"),
                    (u"categoria-240", u"Sympa"),
                    (u"categoria-241", u"Tarifes-Costos Directes"),
                    (u"categoria-242", u"Tarifes-Simulador de costos"),
                    (u"categoria-243", u"Tasques Setmanals"),
                    (u"categoria-244", u"Telefonia"),
                    (u"categoria-245", u"Telefonia SIP - Contact Center HERMES.NET"),
                    (u"categoria-246", u"Teletreball"),
                    (u"categoria-247", u"Televot"),
                    (u"categoria-248", u"Terminal Server"),
                    (u"categoria-249", u"TOAD for Oracle"),
                    (u"categoria-250", u"TOF"),
                    (u"categoria-251", u"Tomcat"),
                    (u"categoria-252", u"TOTQ"),
                    (u"categoria-253", u"Trac"),
                    (u"categoria-254", u"Traveler"),
                    (u"categoria-255", u"Tripwire"),
                    (u"categoria-256", u"Ts"),
                    (u"categoria-257", u"Ubuntu"),
                    (u"categoria-258", u"Univers"),
                    (u"categoria-259", u"Univers.Carnets"),
                    (u"categoria-260", u"UPCconnect"),
                    (u"categoria-261", u"UPClink"),
                    (u"categoria-262", u"videoconferencia"),
                    (u"categoria-263", u"VPN - UPCNET"),
                    (u"categoria-264", u"Web treballar.upc.es"),
                    (u"categoria-265", u"Web UPC"),
                    (u"categoria-266", u"Web UPCnet"),
                    (u"categoria-267", u"webDAV - Accés a repositoris de fitxers (UPC/UPCnet) via web"),
                    (u"categoria-268", u"Web_Edicions"),
                    (u"categoria-269", u"Web_Factorhuma"),
                    (u"categoria-270", u"Web_iEMED"),
                    (u"categoria-271", u"Web_innbox"),
                    (u"categoria-272", u"Windows"),
                    (u"categoria-273", u"Windows 7"),
                    (u"categoria-274", u"Wordpress"),
                    (u"categoria-275", u"X500"),
                    (u"categoria-276", u"Xarxa"),
                    (u"categoria-277", u"Xarxa Troncal"),
                    (u"categoria-278", u"Xarxes LAN"),
                    (u"categoria-279", u"XSF"),
                    (u"categoria-280", u"XSF DIBA"),
                    (u"categoria-281", u"XSFUPC v2.0"),
                    (u"categoria-282", u"Z - Informació obsoleta"),
                    (u"categoria-283", u"Zimbra"),
                    (u"categoria-284", u"(Sin categoría)"),
                       ]
        for keyword in keywords:
            object = _createObjectByType('SimpleVocabularyTerm', category3_keywords, keyword[0])
            object.setTitle(keyword[1])
            object.reindexObject()
    except:
        pass

    #paraules clau CSPT
    try:
        categoryCSPT_keywords = _createObjectByType('SortedSimpleVocabulary', voctool, 'categoryCSPT_keywords')
        keywords = [
                    (u"cspt-01", u"0 - Operativa comuna i informació genèrica"),
                    (u"cspt-02", u"1 - Telecomunicacions"),
                    (u"cspt-03", u"2 - Repositori de fitxers i impressores"),
                    (u"cspt-04", u"3 - Correu electrònic"),
                    (u"cspt-05", u"4 - Administració de Sistemes centrals"),
                    (u"cspt-06", u"Aturar i engegar equips"),
                    (u"cspt-07", u"Dades i persones de contacte CSPT i altres centres"),
                    (u"cspt-08", u"Indicadors"),
                    (u"cspt-09", u"Informació proveïdors"),
                    (u"cspt-10", u"Manuals"),
                    (u"cspt-11", u"Reunions"),
                    (u"cspt-12", u"RRHH"),
                    (u"cspt-13", u"Seguiment UPCnet"),
                    (u"cspt-14", u"Software i utilitats"),
                    (u"cspt-15", u"Startup"),
                    (u"cspt-16", u"Tasques en curs"),
                       ]
        for keyword in keywords:
            object = _createObjectByType('SimpleVocabularyTerm', categoryCSPT_keywords, keyword[0])
            object.setTitle(keyword[1])
            object.reindexObject()
    except:
        pass

    portal.setTitle("Portal Notes")

    langtool = getToolByName(portal, 'portal_languages')
    langtool.manage_setLanguageSettings(defaultLanguage='ca',
                                        supportedLanguages=['ca'],
                                        setUseCombinedLanguageCodes=0,
                                        setForcelanguageUrls=0,
                                        setPathN=1,
                                        setCookieN=1,
                                        setAllowContentLanguageFallback=0,
                                        setRequestN=0,
                                        startNeutral=1,
                                        displayFlags=False)

    plantilles = []
    titol = u"Plantilla KBTIC-RIN"
    resum = u"Per definir un índex amb enllaços al contingut de la mateixa pàgina. Enllaços definits amb àncores."
    cos = u"""<h2>INFORMACIÓ D'ENTRADA (AUS/ADS)</h2>
<h3>Entrades necessàries per a la resolució (i com obtenir-les)</h3>
<p>Morbi dictum. Vestibulum adipiscing pulvinar quam.  In aliquam rhoncus sem. In mi erat, sodales eget, pretium interdum, malesuada  ac, augue. Aliquam sollicitudin, massa ut vestibulum posuere, massa arcu  elementum purus, eget vehicula lorem metus vel libero. Sed in dui id lectus  commodo elementum. Etiam rhoncus tortor. Proin a lorem. Ut nec velit. Quisque  varius. Proin nonummy justo dictum sapien tincidunt iaculis. Duis lobortis  pellentesque risus.</p>
<h3>Requeriments i/o comprovacions prèvies</h3>
<p>Morbi dictum. Vestibulum adipiscing pulvinar quam.  In aliquam  rhoncus sem. In mi erat, sodales eget, pretium interdum, malesuada  ac,  augue. Aliquam sollicitudin, massa ut vestibulum posuere,</p>
<h3>Autoritzacions</h3>
<p>Morbi dictum. Vestibulum adipiscing pulvinar quam.</p>
<h3>Equip a qui assignar el tiquet</h3>
<p>Morbi dictum. Vestibulum adipiscing pulvinar quam.</p>
<p> </p>
<h2>Procediment</h2>
<h4>Sortides (i interpretació i/o tractament)</h4>
<div class="textDestacat">
<p>In aliquam rhoncus sem. Morbi dictum. Vestibulum adipiscing pulvinar quam.  In aliquam rhoncus sem. In mi erat, sodales eget, pretium interdum, malesuada  ac, augue. Aliquam sollicitudin, massa ut vestibulum posuere, massa arcu  elementum purus, eget vehicula lorem metus vel libero. Sed in dui id lectus  commodo elementum. Etiam rhoncus tortor. Proin a lorem. Ut nec velit. Quisque  varius. Proin nonummy justo dictum sapien tincidunt iaculis. Duis lobortis  pellentesque risus.</p>
</div>
<h4>Instruccions de tancament</h4>
<div class="textDestacat">
<p>In aliquam rhoncus sem. Morbi dictum. Vestibulum adipiscing pulvinar  quam.  In aliquam rhoncus sem. In mi erat, sodales eget, pretium  interdum, malesuada  ac, augue. Aliquam sollicitudin, massa ut  vestibulum posuere, massa arcu  elementum purus, eget vehicula lorem  metus vel libero. Sed in dui id lectus  commodo elementum. Etiam rhoncus  tortor. Proin a lorem. Ut nec velit. Quisque  varius. Proin nonummy  justo dictum sapien tincidunt iaculis. Duis lobortis  pellentesque  risus.</p>
</div>
<br />
<div class="llistatIndex">
<h2>Notes d'interés</h2>
<ul>
<li><a href="#">JDuis tellus</a></li>
<li><a href="#">Maecenas elit orci</a></li>
<li><a href="#">At ipsum vitae est lacinia tincidunt</a></li>
</ul>
</div>
<br />"""
    # Prepend to list
    plantilles.insert(0, ({'titol': titol, 'resum': resum, 'cos': cos}))
    # Afegir template KBTIC al TinyMCE
    for plt in plantilles:
        try:
            plantilla = crearObjecte(portal["plantilles"], '', normalizeString(plt['titol']), 'Document', plt['titol'], plt['resum'], '')
            plantilla.setText(plt['cos'], mimetype="text/html")
        except:
            None


def crearObjecte(context, self, id, type_name, title, description, exclude=True, constrains=None):
    pt = getToolByName(context, 'portal_types')
    if not getattr(context, id, False) and type_name in pt.listTypeTitles().keys():
        #creem l'objecte i el publiquem
        _createObjectByType(type_name, context, id)
    #populem l'objecte
    created = context[id]
    doWorkflowAction(context, created)
    created.setTitle(title)
    created.setDescription(description)
    created._at_creation_flag = False
    created.setExcludeFromNav(exclude)
    if constrains:
        created.setConstrainTypesMode(1)
        if len(constrains) > 1:
            created.setLocallyAllowedTypes(tuple(constrains[0] + constrains[1]))
        else:
            created.setLocallyAllowedTypes(tuple(constrains[0]))
        created.setImmediatelyAddableTypes(tuple(constrains[0]))

    created.reindexObject()
    return created


def doWorkflowAction(self, context):
    pw = getToolByName(context, "portal_workflow")
    object_workflow = pw.getWorkflowsFor(context)[0].id
    object_status = pw.getStatusOf(object_workflow, context)
    if object_status:
        try:
            pw.doActionFor(context, {'genweb_simple': 'publish', 'genweb_review': 'publicaalaintranet'}[object_workflow])
        except:
            pass
