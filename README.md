# TP5 : Coding Encoding Decoding

## Sommaire

- [TP5 : Coding Encoding Decoding](#tp5--coding-encoding-decoding)
  - [Sommaire](#sommaire)
- [II. Opti calculatrice](#ii-opti-calculatrice)
- [III. Serveur Web et HTTP](#iii-serveur-web-http)

# II. Opti calculatrice

- [II. Opti calculatrice](#ii-opti-calculatrice)
  - [1. Strings sur mesure](#1-strings-sur-mesure)
  - [2. Code Encode Decode](#2-code-encode-decode)


## 1. Strings sur mesure

🌞 **`tp5_enc_client_1.py`**

[tp5_enc_client_1.py](tp5_enc_client_1.py)

```bash
python tp5_enc_client_1.py
```

🌞 **`tp5_enc_server_1.py`**

[tp5_enc_server_1.py](tp5_enc_server_1.py)

```bash
python tp5_enc_server_1.py
```

## 2. Code Encode Decode

🌞 **`tp5_enc_client_2.py` et `tp5_enc_server_2.py`**

[tp5_enc_client_2.py](tp5_enc_client_2.py)
[tp5_enc_server_2.py](tp5_enc_server_2.py)

```bash
python tp5_enc_server_2.py
python tp5_enc_client_2.py
```

# III. Serveur Web HTTP

Un protocole c'est donc juste des headers, des décisions sur l'encodage, et des données brutes derrière. Genre c'est tout.

Bon bah on va coder un serveur web à la main dukoo. Basique, mais fonctionnel.

Et un navigateur aussi. Un nul, qui supporte rien ou presque, et en ligne de commande.

Faire un vrai navigateur en ligne de commande, genre imiter `curl`, ça demande pas grand chose de plus en terme de cerveau, c'est "juste" des milliers de `if` à rajouter (sans être trop réducteur vis-à-vis de ce beau HTTP).

> Cette section c'est pour montrer aussi les limites de l'encodage opti. Le web c'est trop diversifié comme contenu. Un clieu de MMORPG, tu contrôles exactement ce qu'il t'envoie, et le contenu du jeu, étou. Sur le web, c'est la jungle y'a de tout partout, alors on utilise juste un encodage standard comme UTF-8.

- [III. Serveur Web HTTP](#iii-serveur-web-http)
  - [0. Ptite intro HTTP](#0-ptite-intro-http)
  - [1. Serveur Web](#1-serveur-web)
  - [2. Client Web](#2-client-web)
  - [3. Délivrer des pages web](#3-délivrer-des-pages-web)
  - [4. Quelques logs](#4-quelques-logs)
  - [5. File download](#5-file-download)

## 0. Ptite intro HTTP


## 1. Serveur Web

🌞 **`tp5_web_serv_1.py` un serveur HTTP** super basique

[tp5_web_serv_1.py](tp5_web_serv_1.py)
```bash
python tp5_web_serv_1.py
```

## 2. Client Web

🌞 **`tp5_web_client_2.py` un client HTTP** super basique

[tp5_web_client_2.py](tp5_web_client_2.py)
```bash
python tp5_web_client_2.py
```

## 3. Délivrer des pages web

🌞 **`tp5_web_serv_3.py`**

[tp5_web_serv_3.py](tp5_web_serv_3.py)
```bash
python tp5_web_serv_3.py
```

## 4. Quelques logs

🌞 **`tp5_web_serv_4.py`**

[tp5_web_serv_4.py](tp5_web_serv_4.py)
```bash
python tp5_web_serv_4.py
```

## 5. File download


🌞 **`tp5_web_serv_5.py`**

[tp5_web_serv_5.py](tp5_web_serv_5.py)
[tp5_web_client_5.py](tp5_web_client_5.py)

```bash
python tp5_web_serv_5.py
python tp5_web_client_5.py
```