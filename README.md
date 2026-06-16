# Principes de qualité logicielle et d’architecture

## 1. POO — Programmation orientée objet

La POO consiste à organiser le code autour d’objets qui représentent des concepts métier ou techniques. Un objet regroupe : des données : attributs, propriétés, état ; des comportements : méthodes, actions ; des règles : invariants, validations, responsabilités.

**Objectif :** rendre le code plus structuré, plus maintenable et plus proche du métier.

**Exemple d’application :** éviter un gros fichier qui fait tout, et créer des classes comme User, Booking, PaymentService, PetSitterProfile.

## 2. SOLID

SOLID est un ensemble de 5 principes pour écrire du code orienté objet propre, extensible et maintenable.

### S — Single Responsibility Principle

Une classe doit avoir une seule responsabilité claire.

**Mauvais signe :** une classe qui gère à la fois l’interface, la base de données, les règles métier, les logs et les appels API.

**Bon signe :** une classe BookingService orchestre une réservation, mais ne fait pas directement le paiement Stripe ni l’envoi d’email.

### O — Open/Closed Principle

Le code doit être ouvert à l’extension, mais fermé à la modification. Cela veut dire qu’on doit pouvoir ajouter un comportement sans casser l’existant.

**Exemple :** ajouter un nouveau moyen de paiement via une nouvelle classe plutôt que modifier partout le code existant.

### L — Liskov Substitution Principle

Une classe enfant doit pouvoir remplacer sa classe parente sans casser le comportement attendu. Si une classe hérite d’une autre mais ne respecte pas son contrat, l’héritage est mal conçu.

### I — Interface Segregation Principle

Il vaut mieux plusieurs petites interfaces précises qu’une grosse interface qui force les classes à implémenter des méthodes inutiles.

**Exemple :** séparer Payable, Refundable, Invoiceable au lieu d’avoir une interface énorme PaymentInterface.

### D — Dependency Inversion Principle

Le code métier ne doit pas dépendre directement de détails techniques. Il doit dépendre d’abstractions.

**Exemple :** le domaine dépend d’une interface PaymentProvider, pas directement de StripeClient.

## 3. DRY — Don’t Repeat Yourself

DRY signifie éviter la duplication de logique. Si une règle métier est copiée à plusieurs endroits, elle devient dangereuse : le jour où elle change, tu risques d’oublier une copie.

**Objectif :** centraliser les règles importantes.

**Exemple :** le calcul d’une commission de 15 % doit être dans un seul service ou une seule fonction métier, pas recopié dans trois contrôleurs.

## 4. KISS — Keep It Simple, Stupid

KISS veut dire : faire simple, lisible et compréhensible. Ce n’est pas faire du code basique ou pauvre. C’est éviter les abstractions inutiles, les architectures trop compliquées, les classes créées “au cas où”.

**Objectif :** un autre développeur doit comprendre rapidement ce que fait le code.

**Mauvais signe :** une architecture énorme pour une fonctionnalité simple.

**Bon signe :** une solution claire, directe, testable, sans sur-ingénierie.

## 5. YAGNI — You Aren’t Gonna Need It

YAGNI signifie : ne développe pas une fonctionnalité tant qu’elle n’est pas réellement nécessaire.

**Objectif :** éviter de perdre du temps sur des besoins imaginaires.

**Exemple :** ne pas créer un système complet de coupons, parrainage, abonnement avancé, multi-devises et analytics si le MVP a seulement besoin d’une réservation simple et d’un paiement Stripe test.

## 6. Clean Code

Le Clean Code consiste à écrire du code lisible, compréhensible, cohérent et facile à modifier.

**Cela implique :** des noms explicites ; des fonctions courtes ; des responsabilités bien séparées ; peu d’effets de bord ; pas de logique cachée ; pas de code mort ; pas de duplication inutile ; des erreurs bien gérées.

**Objectif :** le code doit expliquer ce qu’il fait sans nécessiter 50 commentaires.

## 7. Clean Architecture

La Clean Architecture sépare le projet en couches indépendantes.

**Structure typique :** domaine : règles métier pures ; application : cas d’usage ; infrastructure : base de données, API externes, fichiers, Stripe, Supabase ; interface : UI, contrôleurs, routes API.

**Objectif :** éviter que le métier soit mélangé avec la base de données, le framework ou l’interface.

**Exemple :** une règle de réservation ne doit pas être enfermée dans un composant React ou dans une route API Next.js.

## 8. Separation of Concerns — Séparation des responsabilités

Chaque partie du code doit avoir un rôle précis.

**Exemple :** le composant UI affiche ; le service applicatif orchestre ; le domaine valide les règles métier ; le repository lit/écrit les données ; l’adapter Stripe communique avec Stripe.

**Objectif :** éviter les fichiers énormes qui mélangent affichage, logique métier, requêtes SQL et appels réseau.

## 9. SRP — Single Responsibility Principle

Même si c’est déjà dans SOLID, tu le demandes souvent comme règle indépendante. Une fonction, une classe ou un fichier doit avoir une responsabilité principale.

**Mauvais exemple :** MainPage.qml de 1900 lignes qui gère l’affichage, les favoris, le navigateur, les paramètres, les animations, les erreurs et la logique métier.

**Bon exemple :** découper en composants comme BrowserHeader, FavoriteGrid, SearchBar, FaviconImage, BrowserController.

## 10. RAII — Resource Acquisition Is Initialization

RAII est une pratique C++ qui consiste à lier la durée de vie d’une ressource à la durée de vie d’un objet. Quand l’objet est créé, il acquiert la ressource. Quand l’objet est détruit, il libère automatiquement la ressource.

**Ressources concernées :** mémoire ; fichier ; socket ; thread ; mutex ; device caméra ; handle système.

**Objectif :** éviter les fuites mémoire, les ressources non libérées et les crashes.

**Exemple :** utiliser std::unique_ptr, std::shared_ptr, QScopedPointer, QFile, QMutexLocker, plutôt que gérer manuellement des new/delete ou des locks oubliés.

## 11. TDD — Test Driven Development

Le TDD consiste à écrire les tests avant ou en même temps que le code métier.

**Cycle classique :** écrire un test qui échoue ; écrire le minimum de code pour le faire passer ; refactoriser proprement ; recommencer.

**Objectif :** sécuriser les règles importantes et éviter de casser l’existant.

**À utiliser surtout sur :** règles métier ; calculs ; validations ; services critiques ; états de réservation ; permissions ; paiements ; sécurité.

## 12. Tests unitaires

Les tests unitaires vérifient une petite partie isolée du code.

**Objectif :** tester une fonction, une classe ou une règle sans dépendre de la base de données, du réseau ou de l’interface.

**Exemple :** tester que la commission MamiPet vaut bien 15 % du montant de réservation.

## 13. Tests d’intégration

Les tests d’intégration vérifient que plusieurs parties du système fonctionnent ensemble.

**Exemple :** API + base de données ; service de réservation + repository ; Supabase Auth + règles d’accès ; Stripe Connect en mode test + réservation.

**Objectif :** détecter les problèmes entre les couches.

## 14. Tests end-to-end — E2E

Les tests E2E simulent un vrai parcours utilisateur.

**Exemple :** un propriétaire se connecte ; cherche un pet-sitter ; crée une demande ; le pet-sitter accepte ; le propriétaire paie ; la réservation passe au bon statut.

**Objectif :** vérifier que le parcours complet fonctionne.

## 15. Performance

La performance consiste à rendre l’application rapide, fluide et scalable sans gaspiller les ressources.

**Cela concerne :** temps de chargement ; nombre de requêtes ; taille des bundles ; cache ; optimisation SQL ; pagination ; lazy loading ; consommation mémoire ; fluidité UI ; temps de réponse API.

**Objectif :** éviter les lenteurs, les freezes, les surcharges serveur et les interfaces qui rament.

## 16. Quality — Qualité logicielle

La qualité logicielle regroupe tout ce qui rend un projet fiable, maintenable et professionnel.

**Cela inclut :** lisibilité ; testabilité ; sécurité ; performance ; accessibilité ; stabilité ; documentation ; architecture ; robustesse ; cohérence du style.

**Objectif :** produire du code qui peut vivre dans le temps, pas seulement fonctionner vite fait.

## 17. Maintenabilité

La maintenabilité désigne la facilité à modifier, corriger ou faire évoluer le code. Un code maintenable est : bien découpé ; bien nommé ; peu dupliqué ; testé ; documenté quand nécessaire ; prévisible ; peu couplé.

**Objectif :** éviter qu’une modification simple casse tout le projet.

## 18. Scalabilité

La scalabilité est la capacité d’un système à supporter plus d’utilisateurs, plus de données ou plus de trafic sans s’effondrer.

**Cela implique :** architecture propre ; base de données bien modélisée ; index SQL ; cache ; pagination ; jobs asynchrones ; séparation claire des responsabilités ; monitoring.

**Objectif :** éviter que le projet devienne inutilisable dès qu’il grossit.

## 19. Sécurité

La sécurité consiste à protéger les données, les utilisateurs et le système.

**Points importants :** authentification solide ; autorisations strictes ; validation côté serveur ; protection contre injection SQL ; protection XSS ; CSRF selon contexte ; gestion des secrets ; chiffrement quand nécessaire ; logs sans données sensibles ; permissions minimales ; rate limiting ; audit des dépendances.

**Objectif :** ne jamais faire confiance au client, au frontend ou aux données entrantes.

## 20. Least Privilege — Principe du moindre privilège

Chaque utilisateur, service ou composant doit avoir uniquement les droits nécessaires.

**Exemple :** un utilisateur propriétaire ne doit pas pouvoir modifier le profil d’un pet-sitter ou accéder à une réservation qui ne lui appartient pas.

**Objectif :** limiter les dégâts en cas d’erreur ou d’attaque.

## 21. Validation serveur

Toute donnée importante doit être validée côté serveur, même si elle est déjà validée côté frontend. Le frontend peut être contourné.

**Objectif :** empêcher les données invalides, dangereuses ou incohérentes d’entrer dans le système.

## 22. Gestion d’erreurs robuste

Une application professionnelle doit gérer les erreurs proprement.

**Cela implique :** erreurs métier claires ; erreurs techniques séparées ; messages utilisateurs compréhensibles ; logs exploitables ; pas de stack trace exposée ; pas de crash silencieux ; comportements de fallback.

**Objectif :** comprendre les problèmes sans exposer d’informations sensibles.

## 23. Logging

Le logging consiste à enregistrer les événements utiles pour comprendre ce qui se passe. Bons logs : clairs ; structurés ; utiles ; sans données sensibles ; avec contexte ; exploitables en debug ou production.

**Objectif :** pouvoir diagnostiquer un bug sans deviner.

## 24. Observabilité

L’observabilité va plus loin que les logs. Elle regroupe : logs ; métriques ; traces ; alertes ; monitoring ; suivi des erreurs.

**Objectif :** savoir si le système fonctionne réellement en production.

## 25. Documentation technique

La documentation technique explique comment le projet est conçu, installé, lancé, testé et maintenu. Elle doit couvrir : architecture ; installation ; variables d’environnement ; commandes utiles ; choix techniques ; conventions ; déploiement ; tests ; limites connues.

**Objectif :** permettre à un autre développeur de reprendre le projet sans perdre du temps.

## 26. Documentation métier

La documentation métier explique les règles fonctionnelles.

**Exemple :** qui peut réserver ; quand une réservation change de statut ; comment fonctionne la commission ; ce qu’un pet-sitter vérifié peut faire ; quels animaux sont supportés ; quelles validations sont nécessaires.

**Objectif :** éviter que les règles soient seulement cachées dans le code.

## 27. Backend-first

Backend-first signifie concevoir d’abord : le domaine ; les règles métier ; la base de données ; les permissions ; les API ; les tests. Ensuite seulement, on construit le frontend.

**Objectif :** éviter d’avoir une belle interface qui repose sur un modèle fragile ou incohérent. C’est particulièrement important pour des projets comme MamiPet, GameBuilder ou une app métier complexe.

## 28. Domain-driven Design — DDD

Le DDD consiste à organiser le code autour du domaine métier réel. On identifie : les entités ; les value objects ; les agrégats ; les services de domaine ; les événements métier ; les invariants ; les cas d’usage.

**Objectif :** faire correspondre le code au métier, pas seulement à la base de données.

**Exemple MamiPet :** Booking, PetSitterProfile, Animal, VerificationBadge, Payment, Review.

## 29. Modélisation base de données propre

Une base de données propre doit représenter correctement les relations métier.

**Bonnes pratiques :** clés primaires claires ; clés étrangères ; contraintes ; index ; types adaptés ; unicité quand nécessaire ; normalisation raisonnable ; pas de champs fourre-tout ; historiques pour les statuts importants.

**Objectif :** garantir la cohérence des données.

## 30. API Contract First

API Contract First signifie définir les contrats d’API avant de coder au hasard.

**Cela inclut :** routes ; méthodes HTTP ; paramètres ; body ; réponses ; erreurs ; statuts HTTP ; permissions ; règles de validation.

**Objectif :** éviter les API incohérentes et difficiles à consommer côté frontend.

## 31. REST propre

Une API REST propre utilise correctement : les ressources ; les méthodes HTTP ; les statuts ; les URLs ; les erreurs ; la pagination ; les filtres ; l’authentification.

**Exemple :** GET /bookings POST /bookings PATCH /bookings/{id}/accept PATCH /bookings/{id}/cancel

**Objectif :** créer une API lisible, stable et prévisible.

## 32. Idempotence

Une opération idempotente peut être appelée plusieurs fois sans produire plusieurs effets indésirables.

**Exemple :** accepter deux fois la même réservation ne doit pas créer deux paiements ou deux contrats.

**Objectif :** éviter les bugs graves liés aux doubles clics, retries réseau ou appels API répétés.

## 33. Transactions

Une transaction garantit qu’un ensemble d’opérations réussit entièrement ou échoue entièrement.

**Exemple :** lors d’une réservation payée, il ne faut pas enregistrer le paiement si la réservation n’a pas été correctement mise à jour.

**Objectif :** éviter les données incohérentes.

## 34. Migration propre

Les migrations de base de données doivent être : versionnées ; lisibles ; réversibles si possible ; cohérentes ; testées ; sans perte de données non maîtrisée.

**Objectif :** faire évoluer la base sans casser l’application.

## 35. Accessibilité RGAA / WCAG

L’accessibilité consiste à rendre l’interface utilisable par tout le monde, y compris les personnes en situation de handicap.

**Points importants :** HTML valide ; structure sémantique ; titres cohérents ; contrastes suffisants ; labels de formulaire ; alternatives textuelles ; navigation clavier ; focus visible ; messages d’erreur accessibles ; ARIA utilisé correctement ; composants interactifs compréhensibles par les technologies d’assistance.

**Objectif :** conformité RGAA/WCAG et usage réel par tous.

## 36. HTML sémantique

Le HTML sémantique consiste à utiliser les bons éléments pour le bon rôle.

**Exemple :** button pour une action ; a pour une navigation ; label pour un champ ; fieldset et legend pour regrouper des champs ; nav, main, header, footer pour structurer la page.

**Objectif :** améliorer accessibilité, SEO, maintenabilité et robustesse.

## 37. UX — Expérience utilisateur

L’UX consiste à rendre le parcours utilisateur simple, logique et efficace.

**Cela implique :** comprendre le besoin ; réduire la friction ; rendre les actions évidentes ; éviter les ambiguïtés ; fournir des retours visuels ; prévenir les erreurs ; guider sans surcharger.

**Objectif :** l’utilisateur doit savoir quoi faire sans réfléchir inutilement.

## 38. UI — Interface utilisateur

L’UI concerne l’apparence et la lisibilité de l’interface.

**Cela inclut :** typographie ; couleurs ; espacements ; hiérarchie visuelle ; boutons ; cartes ; formulaires ; états hover/focus/disabled ; responsive design ; cohérence graphique.

**Objectif :** une interface claire, moderne, agréable et professionnelle.

## 39. Responsive Design

Le responsive design permet à l’interface de s’adapter aux différentes tailles d’écran.

**Bonnes pratiques :** layout flexible ; grilles adaptatives ; tailles relatives ; breakpoints cohérents ; éviter les débordements ; zones tactiles suffisantes ; priorisation du contenu.

**Objectif :** rendre l’application utilisable sur mobile, tablette et desktop.

## 40. Design System

Un design system définit les règles visuelles et fonctionnelles de l’interface. Il contient : couleurs ; typographies ; espacements ; composants ; états ; règles d’accessibilité ; icônes ; patterns UI.

**Objectif :** éviter les interfaces incohérentes et accélérer le développement.

## 41. Refactorisation

La refactorisation consiste à améliorer la structure du code sans changer son comportement visible.

**Objectif :** réduire la complexité ; découper les responsabilités ; supprimer la duplication ; améliorer la lisibilité ; faciliter les tests ; préparer les évolutions.

**Règle importante :** refactoriser progressivement, avec tests ou vérifications, pour ne pas casser l’existant.

## 42. Couplage faible

Un code faiblement couplé limite les dépendances directes entre modules.

**Objectif :** pouvoir modifier une partie sans casser les autres.

**Exemple :** un service métier ne doit pas dépendre directement d’un composant UI ou d’une librairie externe concrète.

## 43. Cohésion forte

Une classe ou un module a une cohésion forte quand tout ce qu’il contient sert le même objectif.

**Objectif :** éviter les fichiers fourre-tout.

**Bon exemple :** BookingPolicy contient uniquement les règles liées aux réservations.

## 44. Immutabilité

L’immutabilité consiste à éviter de modifier directement les données quand ce n’est pas nécessaire.

**Objectif :** réduire les effets de bord ; rendre le code plus prévisible ; faciliter le debug ; éviter certaines erreurs liées à l’état partagé.

**Exemple :** créer un nouvel état plutôt que modifier silencieusement un objet partagé.

## 45. Thread-safety

La thread-safety garantit que le code fonctionne correctement même quand plusieurs threads l’utilisent. Important en C++/Qt pour : caméra ; threads de traitement ; signaux/slots ; mutex ; accès aux ressources partagées ; arrêt propre des workers.

**Objectif :** éviter les race conditions, freezes, deadlocks et crashs aléatoires.

## 46. Gestion propre du cycle de vie

Un système doit créer, utiliser, arrêter et libérer ses ressources proprement.

**Exemple Qt :** démarrer un thread uniquement quand nécessaire ; arrêter le worker proprement ; fermer la caméra ; libérer le device ; éviter les pointeurs pendants ; supprimer les objets dans le bon thread.

**Objectif :** éviter les crashs, les fuites et les comportements instables.

## 47. CI/CD

CI/CD signifie intégration continue et déploiement continu. Cela permet de : lancer les tests automatiquement ; vérifier le build ; détecter les erreurs tôt ; déployer de manière contrôlée ; automatiser les validations qualité.

**Objectif :** éviter les déploiements manuels risqués.

## 48. Code Review

La revue de code consiste à faire relire le code avant intégration.

**Objectif :** détecter les bugs ; vérifier l’architecture ; améliorer la lisibilité ; partager la connaissance ; éviter les mauvaises pratiques ; garantir la cohérence du projet.

## 49. Convention de nommage

Les noms doivent être explicites, cohérents et adaptés au langage.

**Exemple :** calculateCommissionAmount est meilleur que calc; BookingStatus est meilleur que StatusThing; isKeyboardVisible est meilleur que flag1.

**Objectif :** comprendre le code sans devoir deviner.

## 50. Commentaires utiles

Les commentaires doivent expliquer pourquoi le code existe, pas répéter ce que le code dit déjà. Mauvais commentaire : // increment i Bon commentaire : // Keep the camera device open until the worker thread has fully stopped.

**Objectif :** documenter les décisions, les contraintes et les comportements non évidents.

## 51. Gestion des dépendances

Les dépendances doivent être choisies avec rigueur.

**Critères :** utilité réelle ; maintenance active ; sécurité ; licence ; taille ; compatibilité ; stabilité ; documentation.

**Objectif :** éviter d’alourdir le projet ou d’introduire des risques inutiles.

## 52. Versioning

Le versioning consiste à gérer correctement les versions du code, des APIs, de la base et des dépendances.

**Objectif :** savoir ce qui a changé, pouvoir revenir en arrière, et éviter les ruptures imprévues.

**Exemple :** versionner les routes API en /api/v1.

## 53. Git propre

Bonnes pratiques Git : commits clairs ; branches nommées correctement ; messages explicites ; pas de secrets commités ; pull requests lisibles ; historique compréhensible.

**Objectif :** rendre le projet professionnel et traçable.

## 54. DevSecOps

DevSecOps consiste à intégrer la sécurité dans tout le cycle de développement.

**Cela inclut :** analyse des dépendances ; secrets management ; scans de vulnérabilités ; tests automatisés ; sécurité dans CI/CD ; durcissement des environnements ; monitoring.

**Objectif :** ne pas traiter la sécurité comme une étape finale.

## 55. MVP maîtrisé

Un MVP doit contenir le minimum nécessaire pour valider la valeur du produit, sans surcharger le scope. Cela ne veut pas dire faire un truc sale. Cela veut dire faire peu, mais bien.

**Objectif :** valider rapidement ; réduire le risque ; respecter le temps disponible ; éviter de coder des fonctionnalités inutiles ; garder une base saine pour la suite.

## 56. Priorisation

La priorisation consiste à décider ce qui doit être fait maintenant, plus tard ou jamais.

**Critères :** valeur utilisateur ; risque métier ; risque technique ; coût ; délai ; dépendances ; impact sur le MVP.

**Objectif :** ne pas se disperser.

## 57. Robustesse

La robustesse est la capacité du système à continuer à fonctionner correctement même en cas d’erreur, de donnée inattendue ou de cas limite.

**Exemple :** réseau indisponible ; paiement refusé ; utilisateur non autorisé ; fichier manquant ; caméra inaccessible ; données invalides.

**Objectif :** éviter les crashs et les comportements incohérents.

## 58. Defensive Programming

La programmation défensive consiste à anticiper les entrées invalides et les états impossibles.

**Exemple :** vérifier les null ; vérifier les permissions ; vérifier les statuts ; refuser les transitions invalides ; gérer les erreurs externes.

**Objectif :** ne pas supposer que tout va toujours bien.

## 59. Cohérence frontend/backend

Le frontend ne doit pas inventer des règles différentes du backend. Le backend doit rester la source de vérité.

**Objectif :** éviter les incohérences entre l’affichage et les données réelles.

**Exemple :** si une réservation est refusée côté backend, le frontend ne doit pas pouvoir l’afficher comme acceptée.

## 60. Progressive Enhancement

Le progressive enhancement consiste à construire une base fonctionnelle solide, puis ajouter les améliorations. Exemple web : HTML accessible d’abord ; CSS ensuite ; JS pour améliorer, pas pour rendre tout impossible sans lui.

**Objectif :** rendre l’application plus robuste et accessible.

## 61. Éviter la sur-ingénierie

La sur-ingénierie consiste à créer une architecture trop complexe pour le besoin réel.

**Exemple :** 15 couches abstraites pour afficher une liste simple ; microservices pour un MVP ; patterns inutiles ; génériques partout sans intérêt.

**Objectif :** garder un projet professionnel mais réaliste.

## 62. Architecture modulaire

Une architecture modulaire découpe le projet en blocs indépendants et cohérents.

**Exemple :** auth; booking; payments; profiles; admin; notifications; moderation.

**Objectif :** faciliter l’évolution, les tests et la compréhension.

## 63. CQRS — Command Query Responsibility Segregation

CQRS sépare les opérations de lecture et d’écriture. Command : modifie l’état. Query : lit les données.

**Objectif :** clarifier les intentions et parfois optimiser séparément lecture et écriture. À utiliser quand le domaine devient complexe, pas forcément sur chaque petit projet.

## 64. Event-driven Design

L’event-driven design consiste à déclencher des actions via des événements métier.

**Exemple :** BookingAccepted; PaymentCompleted; ReviewSubmitted; UserVerified.

**Objectif :** découpler les traitements secondaires comme notifications, emails, logs ou analytics.

## 65. Feature Flags

Les feature flags permettent d’activer ou désactiver une fonctionnalité sans redéployer tout le code.

**Objectif :** tester progressivement ; réduire les risques ; désactiver vite une feature cassée ; faire des déploiements contrôlés.

## 66. Pagination

La pagination consiste à ne pas charger toutes les données d’un coup.

**Objectif :** améliorer performance ; réduire la charge serveur ; éviter les interfaces lentes ; limiter les temps de réponse API.

**Exemple :** afficher 20 résultats par page au lieu de charger 10 000 lignes.

## 67. Cache

Le cache garde temporairement des données déjà calculées ou récupérées.

**Objectif :** accélérer les réponses ; réduire les appels API ; soulager la base de données ; améliorer l’expérience utilisateur.

**Attention :** il faut gérer l’invalidation du cache, sinon on affiche des données obsolètes.

## 68. Rate Limiting

Le rate limiting limite le nombre de requêtes autorisées sur une période donnée.

**Objectif :** éviter les abus ; réduire les attaques brute force ; protéger les APIs ; limiter la surcharge serveur.

## 69. Secrets Management

Les secrets sont les clés API, tokens, mots de passe, clés privées.

**Bonnes pratiques :** jamais dans Git ; variables d’environnement ; rotation possible ; accès limité ; séparation dev/preprod/prod ; stockage sécurisé.

**Objectif :** éviter les fuites critiques.

## 70. Environnements séparés

Il faut séparer : développement ; test ; préproduction ; production.

**Objectif :** ne pas tester directement sur la production et éviter les erreurs graves.

## 71. Internationalisation — i18n

L’internationalisation prépare l’application à gérer plusieurs langues.

**Bonnes pratiques :** ne pas coder les textes en dur ; gérer les formats de date ; gérer les devises ; gérer les pluriels ; gérer les textes accessibles.

**Objectif :** permettre une traduction propre sans casser le code.

## 72. Compatibilité

La compatibilité consiste à respecter les versions ciblées. Exemple dans ton cas : Qt 6.8.3 quand tu le demandes ; Qt 6.5.3 quand le projet l’impose ; pas utiliser des APIs incompatibles ; vérifier les modules disponibles ; éviter les dépendances obsolètes.

**Objectif :** fournir du code qui compile réellement dans le contexte cible.

## 73. Déploiement propre

Un déploiement propre doit être reproductible et documenté.

**Cela implique :** variables d’environnement ; scripts ; migrations ; build ; assets ; dépendances ; monitoring ; rollback ; configuration claire.

**Objectif :** éviter le “ça marche sur ma machine”.

## 74. Packaging

Le packaging consiste à préparer l’application pour qu’elle fonctionne hors environnement dev. Dans Qt, cela inclut souvent : DLL ; plugins Qt ; modules QML ; fichiers qmldir; ressources QRC ; assets ; dictionnaires ; plateformes ; dépendances natives.

**Objectif :** éviter une app qui marche en dev mais casse une fois packagée.

## 75. Backward Compatibility

La compatibilité ascendante consiste à éviter de casser les anciens usages quand on fait évoluer une API ou un module.

**Objectif :** permettre aux anciennes parties du système de continuer à fonctionner pendant les évolutions.

## 76. Fail Fast

Fail Fast signifie détecter rapidement les erreurs au lieu de les laisser se propager silencieusement.

**Exemple :** si une variable d’environnement critique manque, l’application doit refuser de démarrer clairement.

**Objectif :** éviter les bugs cachés et difficiles à diagnostiquer.

## 77. Fail Safe

Fail Safe signifie que lorsqu’une erreur arrive, le système se met dans un état sûr.

**Exemple :** si la vérification d’autorisation échoue, refuser l’accès plutôt que l’autoriser.

**Objectif :** préférer un blocage propre à une faille ou une incohérence.

## 78. Atomicité

L’atomicité signifie qu’une opération doit être complète ou ne pas être appliquée du tout. C’est proche du principe de transaction.

**Objectif :** éviter les états partiellement modifiés.

## 79. Invariants métier

Un invariant est une règle qui doit toujours rester vraie.

**Exemple :** une réservation payée doit avoir un paiement valide ; un animal doit appartenir à un propriétaire ; un utilisateur suspendu ne doit pas pouvoir publier une offre ; une réservation acceptée ne doit pas chevaucher une disponibilité déjà bloquée.

**Objectif :** protéger la cohérence métier.

## 80. State Machine — Machine à états

Une machine à états définit les statuts possibles et les transitions autorisées. Exemple réservation : pending_response; accepted; refused; awaiting_payment; paid; cancelled; finished; incident_reported.

**Objectif :** empêcher les transitions absurdes comme passer directement de refused à paid.

## 81. Auditabilité

L’auditabilité consiste à pouvoir retrouver qui a fait quoi, quand, et pourquoi. Important pour : admin ; paiements ; modération ; changements de statut ; sécurité ; RGPD.

**Objectif :** avoir une traçabilité fiable.

## 82. RGPD

Le RGPD impose de protéger les données personnelles.

**Bonnes pratiques :** collecter seulement le nécessaire ; expliquer l’usage ; sécuriser les données ; permettre suppression/export ; limiter la conservation ; protéger les données sensibles ; journaliser les accès critiques.

**Objectif :** respecter les droits utilisateurs et limiter les risques juridiques.

## 83. Typage strict

Le typage strict réduit les erreurs en rendant les contrats explicites.

**Exemple :** TypeScript strict ; enum pour les statuts ; types dédiés pour les IDs ; DTO validés ; modèles clairs.

**Objectif :** détecter les erreurs avant l’exécution.

## 84. DTO — Data Transfer Object

Un DTO définit la forme des données qui entrent ou sortent d’une API ou d’un cas d’usage.

**Objectif :** ne pas exposer directement les entités internes et contrôler précisément les données échangées.

## 85. Repository Pattern

Le repository isole l’accès aux données. Le domaine ou l’application ne doit pas connaître les requêtes SQL exactes ou les détails Supabase/ORM.

**Objectif :** séparer logique métier et persistance.

## 86. Service Layer

La couche service orchestre les cas d’usage.

**Exemple :** CreateBookingService peut vérifier les règles, appeler les repositories, créer le paiement, envoyer un événement.

**Objectif :** éviter de mettre toute la logique dans les contrôleurs ou les composants frontend.

## 87. Adapter Pattern

L’adapter permet d’isoler une dépendance externe.

**Exemple :** StripePaymentAdapter; GoogleMapsGeocodingAdapter; SupabaseStorageAdapter.

**Objectif :** éviter que tout le code dépende directement de l’API d’un fournisseur.

## 88. Dependency Injection

L’injection de dépendances consiste à fournir les dépendances à une classe depuis l’extérieur.

**Objectif :** réduire le couplage ; faciliter les tests ; remplacer facilement une implémentation ; mieux contrôler l’architecture.

## 89. Null Safety

La null safety consiste à éviter les erreurs liées aux valeurs nulles.

**Bonnes pratiques :** types optionnels explicites ; checks clairs ; valeurs par défaut maîtrisées ; pas de null utilisé comme fourre-tout ; erreurs explicites si donnée obligatoire absente.

**Objectif :** éviter les crashs et comportements imprévisibles.

## 90. Linting et formatage

Le linting détecte les problèmes de style, de qualité ou d’erreurs potentielles. Le formatage garantit un style uniforme.

**Objectif :** homogénéiser le code ; éviter les débats inutiles ; détecter certains bugs tôt ; améliorer la lisibilité.

## 91. Static Analysis

L’analyse statique inspecte le code sans l’exécuter. Elle peut détecter : bugs potentiels ; failles ; code mort ; complexité excessive ; erreurs de typage ; problèmes mémoire.

**Objectif :** repérer les défauts avant la production.

## 92. Complexité cyclomatique

La complexité cyclomatique mesure le nombre de chemins possibles dans une fonction. Plus elle est élevée, plus la fonction est difficile à tester et maintenir.

**Objectif :** réduire les gros blocs de conditions imbriquées.

## 93. Simplicité opérationnelle

Un projet doit être simple à lancer, tester et déployer.

**Exemple :** une commande pour installer ; une commande pour lancer ; une commande pour tester ; documentation claire ; .env.example; scripts fiables.

**Objectif :** éviter de perdre du temps sur la configuration.

## 94. Reproductibilité

La reproductibilité signifie que le même projet doit pouvoir fonctionner de la même manière sur une autre machine. Outils utiles : Docker ; lockfiles ; scripts ; CI ; documentation ; versions figées.

**Objectif :** éviter le chaos entre dev, preprod et prod.

## 95. Backups

Les backups protègent les données contre la perte.

**Bonnes pratiques :** sauvegardes automatiques ; tests de restauration ; chiffrement ; conservation maîtrisée ; documentation.

**Objectif :** une sauvegarde non testée ne vaut presque rien.

## 96. Monitoring

Le monitoring surveille l’état du système.

**Exemples :** CPU ; RAM ; disque ; erreurs ; latence ; disponibilité ; jobs échoués ; requêtes lentes.

**Objectif :** détecter les problèmes avant les utilisateurs ou au moins rapidement.

## 97. Progressive Delivery

Le progressive delivery consiste à livrer progressivement une fonctionnalité.

**Exemple :** d’abord en dev ; puis preprod ; puis petit groupe ; puis production complète.

**Objectif :** réduire les risques.

## 98. Graceful Degradation

La graceful degradation consiste à faire en sorte que l’application reste utilisable même si une partie échoue.

**Exemple :** si Google Maps ne charge pas, afficher une liste de résultats géolocalisés approximatifs plutôt qu’une page vide.

**Objectif :** éviter qu’un service externe bloque toute l’application.

## 99. UX Writing

L’UX writing concerne les textes d’interface.

**Bonnes pratiques :** messages clairs ; actions explicites ; erreurs compréhensibles ; pas de jargon inutile ; cohérence de ton ; consignes courtes.

**Objectif :** aider l’utilisateur à comprendre et agir.

## 100. Done propre

Une tâche est vraiment terminée quand : le code fonctionne ; le code est propre ; les tests importants passent ; l’accessibilité est vérifiée ; les erreurs sont gérées ; la documentation utile est mise à jour ; le comportement existant n’est pas cassé ; le résultat correspond au besoin.

**Objectif :** éviter le faux “c’est fini” alors qu’il reste des dettes évidentes.

## 101. Architecture Decision Records — ADR

Les ADR servent à documenter les décisions techniques importantes.

**Un ADR doit expliquer :**

- le contexte ;
- la décision prise ;
- les alternatives envisagées ;
- les conséquences ;
- la date ;
- le statut de la décision.

**Objectif :** éviter de perdre la raison des choix techniques avec le temps.

**Exemple :** documenter pourquoi le projet utilise Supabase plutôt qu’un backend NestJS complet pour le MVP.

## 102. Threat Modeling

Le threat modeling consiste à identifier les menaces possibles avant de coder ou avant de déployer.

**Cela permet d’analyser :**

- les acteurs malveillants ;
- les données sensibles ;
- les points d’entrée ;
- les permissions ;
- les abus possibles ;
- les dépendances externes.

**Objectif :** penser sécurité dès la conception, pas après une faille.

## 103. Secure by Design

Secure by Design signifie que la sécurité doit être intégrée dans l’architecture dès le départ.

**Cela implique :**

- permissions strictes ;
- validation serveur ;
- chiffrement ;
- journalisation ;
- isolation des responsabilités ;
- séparation des environnements ;
- refus par défaut.

**Objectif :** éviter de rajouter la sécurité en rustine à la fin.

## 104. Secure by Default

Secure by Default signifie que la configuration par défaut doit être sûre.

**Exemple :**

- compte privé par défaut ;
- permissions minimales ;
- cookies sécurisés ;
- debug désactivé en production ;
- erreurs techniques non exposées ;
- CORS fermé par défaut.

**Objectif :** éviter qu’un oubli de configuration crée une faille.

## 105. Deny by Default

Toute action non explicitement autorisée doit être refusée.

**Objectif :** éviter les accès involontaires.

**Exemple :** si le backend ne sait pas si l’utilisateur a le droit de lire une réservation, il doit refuser.

## 106. Defense in Depth

La défense en profondeur consiste à multiplier les couches de protection.

**Exemple :**

- validation frontend ;
- validation backend ;
- contraintes base de données ;
- permissions RLS ;
- logs ;
- rate limiting ;
- monitoring ;
- alertes.

**Objectif :** si une couche échoue, une autre limite les dégâts.

## 107. OWASP Top 10

OWASP Top 10 regroupe les risques web les plus critiques.

**Points importants :**

- contrôle d’accès cassé ;
- failles cryptographiques ;
- injections ;
- mauvaise conception de sécurité ;
- mauvaise configuration ;
- dépendances vulnérables ;
- authentification défaillante ;
- intégrité logicielle compromise ;
- logging insuffisant ;
- SSRF.

**Objectif :** vérifier qu’une application web ne contient pas les failles classiques.

## 108. OWASP ASVS

OWASP ASVS fournit une base d’exigences vérifiables pour sécuriser une application.

**Cela couvre :**

- authentification ;
- sessions ;
- contrôle d’accès ;
- validation ;
- cryptographie ;
- API ;
- logs ;
- configuration ;
- gestion des erreurs.

**Objectif :** ne pas se limiter à des conseils vagues, mais vérifier des exigences concrètes.

## 109. RBAC — Role-Based Access Control

RBAC consiste à gérer les permissions selon des rôles.

**Exemple :**

- owner ;
- pet_sitter ;
- admin ;
- moderator ;
- support.

**Objectif :** clarifier qui peut faire quoi.

## 110. ABAC — Attribute-Based Access Control

ABAC va plus loin que RBAC en utilisant des attributs.

**Exemple :**

- un utilisateur peut lire une réservation seulement s’il est le propriétaire, le pet-sitter assigné ou un admin autorisé.

**Objectif :** gérer des règles d’accès plus fines que de simples rôles.

## 111. Row Level Security — RLS

RLS permet de contrôler l’accès aux lignes directement dans la base de données.

Très important avec Supabase/PostgreSQL.

**Objectif :** empêcher qu’un utilisateur lise ou modifie des données qui ne lui appartiennent pas, même si une erreur existe côté API.

## 112. Politique d’autorisation centralisée

Les règles d’autorisation doivent être centralisées et testées.

**Objectif :** éviter que chaque route API réinvente ses propres règles.

**Exemple :** BookingAuthorizationPolicy décide si un utilisateur peut voir, accepter, annuler ou payer une réservation.

## 113. Validation de schéma

Les entrées API doivent être validées avec des schémas stricts.

**Cela concerne :**

- body ;
- query params ;
- path params ;
- headers ;
- webhooks ;
- variables d’environnement.

**Objectif :** refuser rapidement les données invalides.

## 114. Normalisation des entrées

La normalisation consiste à transformer une donnée dans un format propre avant traitement.

**Exemple :**

- email en minuscule ;
- espaces supprimés ;
- dates converties en format standard ;
- numéros de téléphone normalisés.

**Objectif :** éviter les doublons, incohérences et bugs de comparaison.

## 115. Encodage des sorties

L’encodage des sorties consiste à échapper correctement les données affichées.

**Objectif :** éviter les failles XSS.

**Exemple :** ne jamais injecter directement du HTML utilisateur dans une page.

## 116. Sanitization maîtrisée

La sanitization consiste à nettoyer une donnée autorisée.

**Attention :** elle ne remplace pas la validation.

**Objectif :** accepter uniquement ce qui est attendu et nettoyer uniquement quand c’est réellement justifié.

## 117. Content Security Policy — CSP

CSP limite les scripts, styles, images et ressources autorisés par le navigateur.

**Objectif :** réduire l’impact des failles XSS.

## 118. CORS strict

CORS doit autoriser uniquement les origines nécessaires.

**Objectif :** éviter qu’un domaine non autorisé consomme l’API.

## 119. Gestion sécurisée des cookies

Les cookies sensibles doivent être configurés correctement.

**Bonnes pratiques :**

- HttpOnly ;
- Secure ;
- SameSite ;
- durée de vie limitée ;
- rotation de session ;
- pas de données sensibles en clair.

**Objectif :** protéger les sessions utilisateur.

## 120. Gestion robuste des sessions

Une session doit être créée, renouvelée, expirée et invalidée proprement.

**Objectif :** éviter le vol de session et les accès persistants non souhaités.

## 121. MFA — Multi-Factor Authentication

MFA ajoute une vérification supplémentaire lors de la connexion.

**Objectif :** réduire les risques liés au vol de mot de passe.

**Très pertinent pour :**

- admin ;
- support ;
- back-office ;
- actions sensibles ;
- paiements.

## 122. Séparation authentification / autorisation

L’authentification répond à : qui es-tu ?

L’autorisation répond à : as-tu le droit de faire cette action ?

**Objectif :** éviter de croire qu’un utilisateur connecté a automatiquement tous les droits.

## 123. Gestion des secrets avancée

Les secrets doivent être protégés sur tout leur cycle de vie.

**Cela inclut :**

- stockage sécurisé ;
- rotation ;
- révocation ;
- droits limités ;
- audit ;
- séparation par environnement ;
- jamais exposés côté frontend.

**Objectif :** éviter les compromissions critiques.

## 124. Classification des données

Toutes les données ne doivent pas être traitées pareil.

**Catégories possibles :**

- publique ;
- interne ;
- confidentielle ;
- personnelle ;
- sensible ;
- critique.

**Objectif :** appliquer le bon niveau de sécurité selon le type de donnée.

## 125. Minimisation des données

Il faut collecter uniquement les données nécessaires.

**Objectif :** réduire les risques RGPD, sécurité et exploitation.

## 126. Durée de conservation des données

Les données doivent avoir une durée de conservation claire.

**Objectif :** ne pas garder indéfiniment des données inutiles ou sensibles.

## 127. Privacy by Design

La protection de la vie privée doit être pensée dès la conception.

**Cela implique :**

- minimisation ;
- consentement ;
- transparence ;
- sécurité ;
- droits utilisateur ;
- suppression/export ;
- limitation de conservation.

**Objectif :** éviter que le RGPD soit traité comme un simple bandeau cookies.

## 128. AIPD / DPIA

Une analyse d’impact peut être nécessaire si le traitement présente un risque élevé pour les droits et libertés des personnes.

**Objectif :** identifier les risques liés aux données personnelles avant mise en production.

## 129. Chiffrement en transit

Les échanges réseau doivent être protégés par HTTPS/TLS.

**Objectif :** éviter l’interception des données.

## 130. Chiffrement au repos

Les données sensibles stockées doivent être chiffrées quand le contexte l’exige.

**Objectif :** réduire les dégâts en cas de fuite de base ou de stockage.

## 131. Key Management

Les clés de chiffrement doivent être gérées proprement.

**Bonnes pratiques :**

- rotation ;
- accès limité ;
- stockage sécurisé ;
- pas de clé dans Git ;
- séparation par environnement.

**Objectif :** éviter que le chiffrement devienne inutile à cause d’une mauvaise gestion des clés.

## 132. Idempotency Keys

Les opérations critiques doivent utiliser des clés d’idempotence.

**Exemple :**

- paiement ;
- création de réservation ;
- webhook Stripe ;
- acceptation de mission.

**Objectif :** éviter les doubles paiements, doubles réservations et effets répétés après retry.

## 133. Webhooks robustes

Un webhook doit être vérifié et traité proprement.

**Bonnes pratiques :**

- vérifier la signature ;
- enregistrer l’événement reçu ;
- gérer les retries ;
- ignorer les doublons ;
- traiter dans une transaction ;
- journaliser proprement.

**Objectif :** éviter les incohérences avec Stripe, Supabase, GitHub ou tout service externe.

## 134. Outbox Pattern

L’outbox pattern consiste à enregistrer un événement dans la base dans la même transaction que le changement métier.

**Objectif :** éviter qu’une action métier réussisse mais que l’événement associé soit perdu.

## 135. Saga Pattern

Une saga coordonne plusieurs opérations distribuées.

**Exemple :**

- réservation acceptée ;
- paiement créé ;
- notification envoyée ;
- disponibilité bloquée.

**Objectif :** gérer proprement les processus métier qui traversent plusieurs systèmes.

## 136. Retry avec backoff

Les appels réseau qui échouent temporairement peuvent être retentés avec délai progressif.

**Objectif :** éviter d’abandonner trop vite ou de surcharger un service externe.

## 137. Circuit Breaker

Le circuit breaker coupe temporairement les appels vers un service externe défaillant.

**Objectif :** éviter qu’un service externe cassé fasse tomber toute l’application.

## 138. Timeout systématique

Tout appel réseau, base de données ou service externe doit avoir un timeout.

**Objectif :** éviter les blocages infinis.

## 139. Backpressure

Le backpressure consiste à limiter ou ralentir le traitement quand le système est saturé.

**Objectif :** éviter l’effondrement complet sous charge.

## 140. File de jobs

Les tâches longues ou non critiques doivent être mises en file de jobs.

**Exemple :**

- emails ;
- notifications ;
- génération PDF ;
- traitement image ;
- synchronisation externe.

**Objectif :** garder l’API rapide et fiable.

## 141. Health Checks

Une application doit exposer des vérifications de santé.

**Exemples :**

- application démarrée ;
- base accessible ;
- stockage accessible ;
- services critiques disponibles.

**Objectif :** détecter rapidement les problèmes de production.

## 142. Readiness et Liveness

Readiness : l’application est prête à recevoir du trafic.

Liveness : l’application est encore vivante.

**Objectif :** permettre une supervision et un déploiement propres.

## 143. SLI / SLO / SLA

SLI : indicateur mesuré.

SLO : objectif de qualité.

SLA : engagement contractuel.

**Objectif :** mesurer sérieusement la fiabilité.

**Exemple :** 95 % des requêtes API doivent répondre en moins de 300 ms.

## 144. Error Budget

L’error budget définit la marge d’erreur acceptable.

**Objectif :** équilibrer vitesse de livraison et stabilité.

## 145. Incident Response

Il faut prévoir quoi faire en cas d’incident.

**Cela inclut :**

- détection ;
- responsable ;
- priorité ;
- communication ;
- rollback ;
- correction ;
- post-mortem.

**Objectif :** ne pas improviser en production.

## 146. Runbook

Un runbook explique les actions à faire face à un problème connu.

**Objectif :** permettre une réaction rapide même par quelqu’un qui ne connaît pas tout le projet.

## 147. Post-mortem sans blâme

**Après un incident, il faut documenter :**

- ce qui s’est passé ;
- l’impact ;
- la cause ;
- ce qui a bien fonctionné ;
- ce qui doit changer.

**Objectif :** apprendre sans chercher un coupable.

## 148. Rollback Strategy

Chaque déploiement doit pouvoir être annulé proprement.

**Objectif :** limiter l’impact d’une mise en production cassée.

## 149. Migration expand-contract

Une migration compatible production se fait souvent en deux temps.

Expand : ajouter sans casser l’ancien code.

Contract : supprimer l’ancien après transition.

**Objectif :** éviter les coupures lors d’une évolution de base ou d’API.

## 150. Blue/Green Deployment

Le blue/green deployment utilise deux environnements de production alternés.

**Objectif :** basculer rapidement vers une version stable.

## 151. Canary Release

Le canary release expose une nouvelle version à une petite partie des utilisateurs.

**Objectif :** détecter les problèmes avant généralisation.

## 152. Feature Flag Lifecycle

Un feature flag doit avoir une durée de vie limitée.

**Il faut prévoir :**

- création ;
- activation progressive ;
- monitoring ;
- suppression du flag ;
- nettoyage du code mort.

**Objectif :** éviter une dette technique de flags oubliés.

## 153. Contract Testing

Les tests de contrat vérifient que deux systèmes respectent le même contrat.

**Exemple :**

- frontend/API ;
- API/service externe ;
- webhook/handler ;
- microservice/microservice.

**Objectif :** éviter les ruptures d’intégration.

## 154. Property-Based Testing

Le property-based testing génère beaucoup de cas automatiquement pour vérifier une règle générale.

**Objectif :** trouver des cas limites que le développeur n’aurait pas écrits à la main.

## 155. Mutation Testing

Le mutation testing modifie volontairement le code pour vérifier si les tests détectent l’erreur.

**Objectif :** mesurer la vraie qualité des tests.

## 156. Tests de charge

Les tests de charge vérifient le comportement sous trafic important.

**Objectif :** connaître les limites du système.

## 157. Tests de stress

Les tests de stress poussent le système au-delà de ses limites normales.

**Objectif :** comprendre comment il casse.

## 158. Tests de endurance / soak tests

Les tests d’endurance vérifient le comportement sur une longue durée.

**Objectif :** détecter les fuites mémoire, ralentissements progressifs et saturations.

## 159. Profiling

Le profiling consiste à mesurer précisément où le temps CPU, mémoire ou réseau est consommé.

**Objectif :** optimiser ce qui est réellement lent, pas ce qu’on suppose lent.

## 160. Performance Budget

Un budget de performance fixe des limites acceptables.

**Exemple :**

- taille JS maximale ;
- temps de chargement ;
- temps API ;
- nombre de requêtes ;
- poids des images.

**Objectif :** éviter que la performance se dégrade progressivement.

## 161. Memory Leak Detection

Il faut détecter les fuites mémoire, surtout en C++/Qt.

**Outils possibles :**

- AddressSanitizer ;
- ThreadSanitizer ;
- Valgrind ;
- Visual Studio Diagnostics ;
- Qt Creator Analyzer.

**Objectif :** éviter les crashs et pertes de performance dans le temps.

## 162. Concurrency Control

Le contrôle de concurrence évite les conflits quand plusieurs actions arrivent en même temps.

**Exemple :**

- deux utilisateurs acceptent la même disponibilité ;
- deux paiements arrivent ;
- deux webhooks modifient la même réservation.

**Objectif :** éviter les états incohérents.

## 163. Optimistic Locking

L’optimistic locking vérifie qu’une donnée n’a pas changé avant de l’enregistrer.

**Objectif :** éviter d’écraser silencieusement une modification concurrente.

## 164. Pessimistic Locking

Le pessimistic locking bloque temporairement une ressource pendant une opération critique.

**Objectif :** protéger une action qui ne supporte pas la concurrence.

## 165. Gestion stricte des statuts métier

Les statuts métier doivent être définis avec des enums ou types stricts.

**Objectif :** éviter les chaînes magiques et les statuts invalides.

## 166. Horodatage fiable

Les dates importantes doivent être stockées proprement.

**Bonnes pratiques :**

- UTC en base ;
- timezone IANA côté affichage ;
- pas de date locale ambiguë ;
- horodatage serveur pour les événements critiques.

**Objectif :** éviter les bugs de fuseau horaire, réservation et audit.

## 167. Gestion des montants financiers

Les montants financiers ne doivent pas être gérés avec des flottants.

**Bonnes pratiques :**

- entiers en centimes ;
- Decimal adapté ;
- devise explicite ;
- arrondis contrôlés ;
- tests sur les calculs.

**Objectif :** éviter les erreurs de paiement et de commission.

## 168. Value Objects

Un value object représente une valeur métier contrôlée.

**Exemples :**

- EmailAddress ;
- Money ;
- DateRange ;
- BookingPeriod ;
- UserId ;
- PetWeight.

**Objectif :** éviter les primitives non validées partout dans le code.

## 169. Strongly Typed IDs

Les identifiants doivent être typés quand possible.

**Exemple :** UserId ne doit pas être confondu avec BookingId.

**Objectif :** éviter les erreurs de passage d’identifiants.

## 170. Boundary Testing

Les tests doivent couvrir les limites.

**Exemple :**

- montant à 0 ;
- date passée ;
- date égale à la limite ;
- texte trop long ;
- liste vide ;
- utilisateur suspendu ;
- paiement refusé.

**Objectif :** éviter les bugs dans les cas limites.

## 171. Test Pyramid

**La stratégie de tests doit équilibrer :**

- beaucoup de tests unitaires ;
- moins de tests d’intégration ;
- quelques tests E2E critiques.

**Objectif :** avoir des tests rapides, fiables et utiles.

## 172. Tests d’accessibilité automatisés

Les outils automatisés peuvent détecter une partie des erreurs d’accessibilité.

**Objectif :** attraper rapidement les erreurs simples.

**Attention :** ils ne remplacent pas les tests manuels clavier, lecteur d’écran et analyse RGAA.

## 173. Tests clavier

Une interface doit être utilisable au clavier.

**Objectif :** vérifier la navigation, le focus, l’ordre logique et l’accès aux actions.

## 174. Tests lecteur d’écran

Les parcours importants doivent être testés avec un lecteur d’écran.

**Objectif :** vérifier que l’interface est réellement compréhensible, pas seulement valide techniquement.

## 175. API Deprecation Policy

Une API doit avoir une stratégie de dépréciation.

**Cela inclut :**

- version ;
- date de fin ;
- documentation ;
- compatibilité ;
- migration.

**Objectif :** éviter de casser les clients brutalement.

## 176. Backward-Compatible API Changes

Les évolutions d’API doivent rester compatibles autant que possible.

**Exemple :** ajouter un champ optionnel est moins risqué que renommer un champ existant.

**Objectif :** réduire les ruptures côté frontend ou clients externes.

## 177. Compatibility Matrix

Une matrice de compatibilité liste les versions supportées.

**Exemple :**

- Qt 6.8.3 ;
- Node.js 22 ;
- PostgreSQL 16 ;
- Windows 11 ;
- Android cible ;
- navigateurs supportés.

**Objectif :** éviter les ambiguïtés sur ce qui doit réellement fonctionner.

## 178. SBOM — Software Bill of Materials

Un SBOM liste les composants et dépendances d’un logiciel.

**Objectif :** savoir rapidement quelles dépendances sont utilisées en cas de faille.

## 179. Licence Compliance

Chaque dépendance doit avoir une licence compatible avec le projet.

**Objectif :** éviter les problèmes juridiques.

## 180. Supply Chain Security

La sécurité de la chaîne logicielle protège contre les dépendances compromises.

**Bonnes pratiques :**

- lockfiles ;
- versions figées ;
- audit dépendances ;
- revue des packages ;
- pas de dépendance inutile ;
- vérification des mainteneurs.

**Objectif :** éviter d’introduire une faille par une librairie externe.

## 181. Revue des dépendances

Toute nouvelle dépendance doit être justifiée.

**Critères :**

- besoin réel ;
- maintenance ;
- taille ;
- sécurité ;
- licence ;
- compatibilité ;
- alternative native.

**Objectif :** éviter d’alourdir le projet inutilement.

## 182. Configuration as Code

La configuration importante doit être versionnée et documentée.

**Objectif :** rendre les environnements reproductibles.

## 183. Infrastructure as Code

L’infrastructure doit être décrite par du code quand le projet le justifie.

**Objectif :** éviter les configurations manuelles impossibles à reproduire.

## 184. Environnements éphémères

Un environnement temporaire peut être créé pour tester une branche ou une pull request.

**Objectif :** valider une fonctionnalité avant merge ou production.

## 185. Seed Data maîtrisée

Les données de test doivent être reproductibles.

**Objectif :** tester le projet dans un état connu.

## 186. Fixtures propres

Les fixtures doivent représenter des cas réalistes et utiles.

**Objectif :** éviter les tests basés sur des données incohérentes.

## 187. Documentation d’exploitation

La documentation ne doit pas seulement expliquer le code.

**Elle doit aussi expliquer :**

- comment déployer ;
- comment surveiller ;
- comment restaurer ;
- comment diagnostiquer ;
- comment rollback.

**Objectif :** rendre le projet exploitable en production.

## 188. Documentation des erreurs connues

Les limitations et erreurs connues doivent être documentées.

**Objectif :** éviter de redécouvrir les mêmes problèmes.

## 189. Changelog

Le changelog documente les changements importants.

**Objectif :** savoir ce qui a changé entre deux versions.

## 190. Release Notes

Les release notes expliquent une livraison de manière exploitable.

**Cela inclut :**

- nouvelles fonctionnalités ;
- corrections ;
- ruptures ;
- migrations ;
- risques ;
- actions nécessaires.

**Objectif :** rendre les livraisons compréhensibles.

## 191. Code Ownership

Chaque partie importante du code doit avoir un responsable ou référent.

**Objectif :** éviter les zones critiques sans propriétaire.

## 192. Definition of Ready

Une tâche est prête quand le besoin est clair avant développement.

**Cela inclut :**

- objectif ;
- règles métier ;
- critères d’acceptation ;
- maquettes si nécessaire ;
- contraintes ;
- dépendances ;
- cas limites connus.

**Objectif :** éviter de coder sur une demande floue.

## 193. Critères d’acceptation

Les critères d’acceptation définissent comment vérifier qu’une tâche est réussie.

**Objectif :** éviter les validations subjectives.

## 194. Risk-Based Development

Les tâches doivent être priorisées selon le risque.

**Risques possibles :**

- technique ;
- métier ;
- sécurité ;
- planning ;
- performance ;
- dépendance externe.

**Objectif :** traiter tôt ce qui peut bloquer le projet.

## 195. Technical Spike

Un spike est une exploration courte pour réduire une incertitude technique.

**Objectif :** éviter de s’engager sur une solution non vérifiée.

## 196. Limitation volontaire du scope

Le scope doit être défini explicitement.

**Objectif :** éviter que le MVP grossisse sans contrôle.

## 197. Anti-Corruption Layer

Une couche anti-corruption protège le domaine contre un modèle externe mal adapté.

**Exemple :** ne pas laisser le modèle Stripe ou Supabase polluer directement les entités métier.

**Objectif :** garder un domaine propre malgré les dépendances externes.

## 198. Hexagonal Architecture

L’architecture hexagonale sépare le cœur métier des dépendances externes via des ports et adapters.

**Objectif :** rendre le domaine testable et indépendant du framework.

## 199. Ports and Adapters

Un port définit ce dont l’application a besoin.

Un adapter implémente ce port avec une technologie concrète.

**Exemple :**

- PaymentProvider est un port ;
- StripePaymentAdapter est un adapter.

**Objectif :** découpler le métier de l’infrastructure.

## 200. Dependency Rule

Les dépendances doivent aller vers le domaine, jamais l’inverse.

**Objectif :** éviter que le métier dépende de React, Next.js, Supabase, Stripe ou Qt.

## 201. Bounded Context

Un bounded context définit une zone métier avec son propre vocabulaire et ses propres règles.

**Exemple :**

- booking ;
- payments ;
- profiles ;
- notifications ;
- moderation.

**Objectif :** éviter un modèle unique trop gros et confus.

## 202. Ubiquitous Language

Le vocabulaire utilisé dans le code doit correspondre au vocabulaire métier.

**Objectif :** réduire l’écart entre métier, documentation et code.

## 203. Event Storming

L’event storming permet de modéliser un domaine à partir des événements métier.

**Exemple :**

- BookingRequested ;
- BookingAccepted ;
- PaymentAuthorized ;
- ReviewSubmitted.

**Objectif :** mieux comprendre les processus avant de coder.

## 204. CQRS raisonnable

CQRS doit être utilisé quand la séparation lecture/écriture apporte une vraie valeur.

**Objectif :** éviter d’appliquer CQRS partout par mode.

## 205. Read Model

Un read model est une structure optimisée pour la lecture.

**Objectif :** éviter de complexifier le domaine uniquement pour afficher une page.

## 206. Command Handler

Un command handler traite une intention de modification.

**Exemple :**

- AcceptBookingCommandHandler ;
- CancelBookingCommandHandler.

**Objectif :** isoler les cas d’usage d’écriture.

## 207. Query Handler

Un query handler traite une demande de lecture.

**Exemple :**

- GetPetSitterProfileQueryHandler.

**Objectif :** clarifier les opérations de lecture.

## 208. Error Taxonomy

Les erreurs doivent être classées.

**Exemples :**

- erreur métier ;
- erreur validation ;
- erreur autorisation ;
- erreur technique ;
- erreur externe ;
- erreur système.

**Objectif :** gérer proprement les réponses API, logs et messages utilisateur.

## 209. Domain Errors

Les erreurs métier doivent être explicites.

**Exemple :**

- BookingAlreadyAccepted ;
- PaymentAlreadyCaptured ;
- UserNotAllowed ;
- InvalidBookingPeriod.

**Objectif :** éviter les erreurs génériques incompréhensibles.

## 210. Résilience UI

L’interface doit gérer les états incomplets.

**Exemples :**

- chargement ;
- erreur ;
- vide ;
- hors ligne ;
- permission refusée ;
- donnée supprimée ;
- retry possible.

**Objectif :** éviter les écrans cassés ou incompréhensibles.

## 211. Skeleton Loading

Le skeleton loading affiche une structure temporaire pendant le chargement.

**Objectif :** améliorer la perception de fluidité.

## 212. Empty States

Les états vides doivent être conçus.

**Exemple :** aucune réservation, aucun favori, aucun résultat.

**Objectif :** guider l’utilisateur au lieu d’afficher une page vide.

## 213. Offline Strategy

Certaines applications doivent prévoir le comportement hors ligne.

**Objectif :** éviter les erreurs brutales en cas de réseau instable.

## 214. Image Optimization

Les images doivent être optimisées.

**Bonnes pratiques :**

- formats modernes ;
- compression ;
- lazy loading ;
- dimensions adaptées ;
- alt text ;
- cache.

**Objectif :** améliorer performance, accessibilité et SEO.

## 215. SEO technique

Pour un site public, le SEO technique doit être propre.

**Cela inclut :**

- titres ;
- meta descriptions ;
- structure HTML ;
- données structurées ;
- robots ;
- sitemap ;
- canonical ;
- performance ;
- accessibilité.

**Objectif :** rendre le site compréhensible par les moteurs de recherche.

## 216. Données structurées

Les données structurées aident les moteurs à comprendre le contenu.

**Objectif :** améliorer la compréhension SEO quand le contexte s’y prête.

## 217. Internationalisation technique

L’i18n doit être pensée proprement.

**Cela inclut :**

- traductions centralisées ;
- formats de dates ;
- devises ;
- pluriels ;
- direction du texte ;
- accessibilité des textes.

**Objectif :** éviter une traduction bricolée.

## 218. Timezone Strategy

La gestion des fuseaux horaires doit être définie.

**Règle courante :**

- stockage UTC ;
- affichage selon timezone utilisateur ;
- timezone métier explicite pour les réservations.

**Objectif :** éviter les bugs de dates dans les réservations, paiements et notifications.

## 219. Monetary Strategy

La gestion des devises doit être explicite.

**Bonnes pratiques :**

- montant en centimes ;
- devise obligatoire ;
- arrondis maîtrisés ;
- pas de float ;
- tests dédiés.

**Objectif :** éviter les erreurs financières.

## 220. IA Assistée — règles de contrôle

Le code généré par IA doit être contrôlé comme du code humain.

**Règles :**

- ne pas faire confiance aveuglément ;
- vérifier les APIs ;
- compiler ;
- tester ;
- relire ;
- contrôler sécurité ;
- contrôler accessibilité ;
- contrôler cohérence architecture.

**Objectif :** éviter d’introduire du code faux mais plausible.

## 221. IA — interdiction d’inventer

L’IA ne doit pas inventer une API, une méthode, une dépendance ou une règle métier.

**Objectif :** éviter les hallucinations techniques.

Si une information est incertaine, elle doit être vérifiée ou signalée.

## 222. IA — respect strict du contexte projet

**L’IA doit respecter :**

- version cible ;
- framework ;
- structure existante ;
- noms existants ;
- contraintes métier ;
- style de code ;
- architecture ;
- fichiers déjà modifiés.

**Objectif :** éviter les solutions génériques qui cassent le projet réel.

## 223. IA — modification minimale contrôlée

L’IA doit modifier uniquement ce qui est nécessaire.

**Objectif :** éviter les refontes inutiles, les régressions et les changements cachés.

## 224. IA — code complet et compilable

Quand une correction de code est demandée, l’IA doit fournir des fichiers complets ou un patch exploitable.

**Objectif :** éviter les extraits impossibles à intégrer.

## 225. IA — explication des impacts

**Toute proposition technique doit expliquer :**

- ce qui change ;
- pourquoi ;
- risques ;
- tests à faire ;
- effets secondaires ;
- compatibilité.

**Objectif :** permettre une décision technique sérieuse.

## 226. IA — pas de dépendance inutile

L’IA ne doit pas ajouter une dépendance sans justification forte.

**Objectif :** éviter d’alourdir le projet ou d’introduire des risques.

## 227. IA — conservation du comportement existant

Une correction ne doit pas casser les fonctionnalités déjà présentes.

**Objectif :** éviter les régressions silencieuses.

## 228. IA — vérification des versions

L’IA doit vérifier la compatibilité avec les versions demandées.

**Exemple :**

- Qt 6.8.3 ;
- Qt 6.5.3 ;
- Next.js version cible ;
- Node.js version cible ;
- Supabase version cible.

**Objectif :** éviter du code qui ne compile pas ou ne fonctionne pas.

## 229. IA — production-ready par défaut

L’IA doit éviter le code de démonstration quand le besoin est professionnel.

**Cela implique :**

- gestion d’erreurs ;
- types stricts ;
- tests ;
- sécurité ;
- accessibilité ;
- structure propre ;
- pas de TODO bloquant.

**Objectif :** produire du code réellement intégrable.

## 230. IA — signalement des incertitudes

L’IA doit dire clairement ce qui est certain, incertain ou à vérifier.

**Objectif :** éviter les réponses confiantes mais fausses.

## 231. IA — priorité aux standards

**L’IA doit privilégier :**

- documentation officielle ;
- standards reconnus ;
- bonnes pratiques éprouvées ;
- solutions simples ;
- compatibilité projet.

**Objectif :** éviter les solutions fantaisistes.

## 232. IA — refus des raccourcis sales

**L’IA ne doit pas proposer une solution rapide qui dégrade fortement :**

- sécurité ;
- maintenabilité ;
- accessibilité ;
- architecture ;
- données ;
- performance.

**Objectif :** éviter une dette technique dangereuse.

## 233. IA — tests associés aux corrections

Toute correction importante doit être accompagnée d’une stratégie de test.

**Objectif :** prouver que la correction fonctionne et ne casse pas l’existant.

## 234. IA — documentation des choix

L’IA doit proposer de documenter les choix importants quand ils impactent l’architecture.

**Objectif :** garder une trace utile pour le projet.

## 235. IA — revue critique

L’IA doit être capable de dire qu’une demande est mauvaise techniquement si elle l’est.

**Objectif :** éviter d’exécuter aveuglément une mauvaise décision.

## 236. IA — priorité au métier

L’IA doit comprendre le besoin métier avant de proposer une structure technique.

**Objectif :** éviter une architecture jolie mais déconnectée de l’usage réel.

## 237. IA — pas de sur-ingénierie automatique

L’IA doit adapter la solution au contexte réel.

**Objectif :** ne pas proposer microservices, CQRS, event sourcing ou abstractions complexes sans besoin prouvé.

## 238. IA — sécurité et accessibilité non optionnelles

L’IA doit intégrer sécurité et accessibilité comme contraintes normales du développement.

**Objectif :** éviter de traiter ces sujets comme des bonus.

## 239. IA — cohérence globale

**L’IA doit garder la cohérence entre :**

- code ;
- base de données ;
- API ;
- frontend ;
- tests ;
- documentation ;
- déploiement.

**Objectif :** éviter les solutions correctes localement mais incohérentes globalement.

## 240. IA — résultat vérifiable

**Toute proposition doit pouvoir être vérifiée par :**

- build ;
- tests ;
- lint ;
- analyse statique ;
- audit ;
- validation manuelle ;
- critères d’acceptation.

**Objectif :** éviter les réponses non mesurables.

## 241. FinOps

FinOps consiste à surveiller et optimiser les coûts techniques.

**Cela concerne :**

- hébergement ;
- base de données ;
- stockage ;
- logs ;
- API externes ;
- builds CI ;
- CDN ;
- services cloud.

**Objectif :** éviter qu’un projet devienne trop coûteux sans contrôle.

## 242. Quotas et limites externes

Les limites des services externes doivent être connues.

**Exemple :**

- Stripe ;
- Supabase ;
- Google Maps ;
- Firebase ;
- Vercel ;
- API email.

**Objectif :** éviter les blocages en production.

## 243. Vendor Lock-in maîtrisé

Le vendor lock-in doit être assumé ou limité.

**Objectif :** savoir ce qui dépend fortement d’un fournisseur externe.

## 244. Plan de sortie

Pour une dépendance critique, il faut savoir comment migrer si nécessaire.

**Objectif :** éviter d’être bloqué par un fournisseur.

## 245. Data Portability

Les données importantes doivent pouvoir être exportées proprement.

**Objectif :** conformité, maintenance et liberté technique.

## 246. Qualité des données

La qualité des données doit être surveillée.

**Cela inclut :**

- doublons ;
- valeurs invalides ;
- données obsolètes ;
- relations cassées ;
- statuts incohérents.

**Objectif :** éviter qu’une base propre au départ devienne inutilisable.

## 247. Contraintes base de données

La base doit protéger les règles critiques.

**Exemples :**

- foreign keys ;
- unique constraints ;
- check constraints ;
- not null ;
- index ;
- transactions.

**Objectif :** ne pas laisser toute la cohérence uniquement au code applicatif.

## 248. Indexation maîtrisée

Les index doivent être ajoutés selon les requêtes réelles.

**Objectif :** améliorer les performances sans ralentir inutilement les écritures.

## 249. Requêtes SQL analysées

Les requêtes importantes doivent être analysées.

**Objectif :** détecter les scans complets, jointures coûteuses et index manquants.

## 250. Nettoyage de dette technique

La dette technique doit être identifiée, priorisée et traitée.

**Objectif :** éviter qu’elle devienne invisible puis ingérable.
