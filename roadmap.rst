

=============
API FusionPBX
=============

por Gnovit https://gnovit.com

Autor: Marcelo Araujo marcelo@gnovit.com

versão do documento: 0.1 (rascunho) - 17/07/2023


Objetivo
--------

Prover uma interface http para o FusionPBX para que seja possível a administração do FusionPBX.

Será feito em Python com framwork fastapi, o mesmo já utilizado no webserver do Freeswitch Rabbit connector. 
A interação se dará utilizando-se a interface web do FusionPBX com o uso da biblioteca Selenium.

Na primeira etapa do projeto serão providos os serviços de CRUD: Create, Read, Update e Delete para as seguintes entidades:

- Domínios
- Ramais

Essa será considerada a versão 1.0
Para as próximas versões serão analisadas as necessidades pelos times de suporte e desenvolvimento da Seventh.

Entrega
-------

A entrega será feita em Container Docker para que possa ser utilizado em qualquer ambiente do cliente.