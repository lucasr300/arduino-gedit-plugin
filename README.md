# Arduino gEdit Plugin
Por: Lucas R. Martins

Um plugin para o gEdit que permite você compilar e fazer upload do seu código direto para o Arduino :-)


## How to install

* Basta copiar todos os arquivos para o diretório / . Em seguida, é necessário ativar o plugin no menu Editar > Preferências > Plugins do GEdit

* Dependências: avr-libc, avrdude, gcc, gcc-avr. Enquanto não temos um pacote, é necessário instalar esses pacotes manualmente, mas isso é uma questão de tempo.

* Uma vez instalado, basta pressionar a tecla F7 para compilar e enviar o código para o arduino. As opções aparecem no menu Ferramentas do GEdit



## Known Bugs

* Devido a uma limitação do gEdit, o plugin as vezes não salva o arquivo automaticamente.

* Atualmente só compila código para o Arduino com AtMega328. 
 


## Warnings

* Foi testado apenas com meu Arduino. Pode não funcionar com o seu.


