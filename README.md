Oppgave 1

a) HTTP Endepunkt for lambdafunksjon som kan testes med Postman:

https://n60393cta5.execute-api.eu-west-1.amazonaws.com/Prod/generate-image

(AWS access og secret keys ligger tilgjengelig i .txt filen for sikkerhets-
messige årsaker, vil ikke legge det til på GitHub hvor bots kan finne dem)

b) Lenke til kjørt GitHub Actions workflow (som har deployet SAM-applikasjone):
https://github.com/henaaro/devops/actions/runs/11910430238

---

Oppgave 2

a) Kode finnes i mappen "infra", i main.tf
b) Lenke til kjørt Actions workflow:
https://github.com/henaaro/devops/actions/runs/11914158217

Lenke til fungerende GitHub Actions workflow (ikke main):
https://github.com/henaaro/devops/actions/runs/11920602646

SQS-Kø URL:
https://sqs.eu-west-1.amazonaws.com/160885256027/image-processing-queue

---

Oppgave 3
a) Koden finnes i filen "Dockerfile" i mapppen java_sqs_client
b) Hvordan jeg har valgt å tagge container imagene mine og hvorfor:
1. Latest Tag  
        Latest tagggen representerer den nyeste versjonen av docker
        imaget. Når en ny commit blir pusha, bllir imaget bygget og
        tagget med main. Da blir det enkelt for teamet å alltid få
        tilggang til den siste stabile versjonen av imaget.
2. "<commit-sha>" tag:
        Hver gang jeg commiter blir en unik sha-hash generert, så jeg
        valgte å bruke denne hashen som en tag for docker imaget. Da
        blir det mulig å identifisere og referere til eksakte versjoner
        av imaget knyttet till spesifikke commits. Dette hjelper når det
        gjelder feilsøking ogg presis versjonskontroll.


Docker image:
waaro/java-sqs-client

(AWS access og secret keys liggger fremdeles tilgjengelig i .txt filen)

---

Oppgave 4

![img.png](img.png)
Har lagt til min egen mail her, så vet ikke helt hvordan det vil være for sensor
å sjekke at det funker, men koden ligger i:
main.tf, variables.tf og terraform.tfvars
Som en kan se på bildet over, og muligens på AWS panelet, kan man se at mailen sendes
når kravene er oppfylt.


---

Oppgave 5