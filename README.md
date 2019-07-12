# Scuolabook Downloader with Firefox headless browser
Scarica i tuoi libri in PDF per uso offline e personale.<br>
Download your books in PDF format for personal and offline use.

**[ITALIANO]**

**_NOTA: Progetto in fase di testing_**

Il progetto Scuolabook Downloader nasce dalla necessità di scaricare in formato PDF i libri scolastici acquistati, mettendo "da parte" il lettore di Scuolabook che necessita l'accesso ad Internet.

**_Requisiti:_**
<ul>
  <li>Firefox 56+</li>
  <li>Geckodriver Firefox &nbsp; &nbsp; https://github.com/mozilla/geckodriver/releases</li>
  <li>Python 3.x &nbsp; &nbsp; https://www.python.org/downloads/</li>
  <li>Selenium &nbsp; &nbsp; &nbsp; <code>pip install selenium</code></li>
  <li>img2pdf &nbsp; &nbsp; &nbsp; <code>pip install img2pdf</code></li>
</ul>

**_Come utilizzare il programma:_**
<ol>
  <li> Modificare riga <code>27</code> (specificare percorso Geckodriver) e <code>98</code> (specificare nome utente)
  <li> Inserisci le credenziali di accesso al tuo account Scuolabook.</li>
  <li> Inserisci il codice del libro che vuoi scaricare.</li>
  <li> Attendi che il programma scarichi le pagine del libro e le unisca in un unico PDF.</li>
</ol>
