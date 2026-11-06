---
layout: post
title: "ISS Deluxe – American Restored Edition: preservando um clássico do futebol no SNES"
date: 2026-11-06
categories:
  - Projetos
permalink: /iss-deluxe-american-restored-edition/
excerpt: "Conheça a primeira etapa do projeto de restauração de International Superstar Soccer Deluxe: uma edição baseada na ROM americana, com foco em preservação, investigação técnica e melhorias cuidadosamente planejadas."
related_project: /projetos/iss-deluxe-american-restored-edition/
---

<figure class="article-hero">
  <img src="https://images.igdb.com/igdb/image/upload/t_1080p_2x/bytlgkgtbmolnc9cvvp7.webp" alt="Partida entre Brasil e Itália em International Superstar Soccer Deluxe no Super Nintendo">
  <figcaption>Uma partida de International Superstar Soccer Deluxe. Imagem de referência do jogo original — <a href="https://backloggd.com/games/international-superstar-soccer-deluxe/" target="_blank" rel="noopener">Backloggd / IGDB</a>.</figcaption>
</figure>

Há jogos que marcaram uma geração não apenas pelo que ofereciam, mas pela maneira como faziam cada partida parecer um acontecimento. **International Superstar Soccer Deluxe**, da Konami, é um desses nomes. No Super Nintendo, o jogo conquistou espaço com partidas movimentadas, seleções nacionais, opções táticas e uma apresentação que ainda hoje carrega a identidade dos grandes títulos esportivos da era 16-bit.

O Covil Secreto inicia um trabalho dedicado a esse clássico: **ISS Deluxe – American Restored Edition**. A proposta é estudar a edição americana, preservar sua identidade e investigar, com cuidado, possibilidades de restauração a partir da comparação técnica com a edição japonesa.

## Uma edição americana como ponto de partida

A primeira decisão do projeto é também a mais importante: a ROM americana será a base de todo o trabalho. Isso significa manter o idioma, a estrutura e as características que definem essa edição, em vez de simplesmente substituí-la por outra versão.

A edição japonesa será utilizada como material de referência. As diferenças entre as duas serão examinadas para entender o que realmente mudou entre os lançamentos. Uma diferença encontrada não será tratada automaticamente como conteúdo removido: primeiro será necessário compreender sua função, sua estrutura e se existe uma forma segura de aproveitá-la.

<figure>
  <img src="https://atomix.blob.core.windows.net/images/uploads/2014/05/international-superstar-soccer-deluxe-carboni-galfano.jpg" alt="Tela de seleção de equipes e formação de International Superstar Soccer Deluxe">
  <figcaption>Menu de seleção e formação: uma das áreas que ajudam a ilustrar a variedade de sistemas presentes no jogo. Imagem de referência publicada pela <a href="https://atomix.vg/feature-snes-international-superstar-soccer-y-yo" target="_blank" rel="noopener">Atomix</a>.</figcaption>
</figure>

## O trabalho começa pela investigação

Antes de alterar gráficos, textos ou áudio, a restauração precisa entender como o jogo está organizado. O levantamento inicial das ROMs já aponta diferenças relevantes de tamanho e configuração:

- **Edição americana:** imagem de 2 MiB, mapeamento LoROM e sem SRAM.
- **Edição japonesa:** imagem de 3 MiB (4 MiB quando considerada com cabeçalho), também em LoROM, com SRAM de 8 KiB e suporte a bateria.

Esses dados ajudam a definir o caminho técnico. A decisão atual é manter o projeto em **LoROM**, sem migrar para HiROM. A expansão de capacidade exige adaptar e testar corretamente o acesso aos bancos adicionais; não basta aumentar o tamanho do arquivo e presumir que o console reconhecerá todo o conteúdo.

## O que queremos investigar e restaurar

A primeira fase está organizada em frentes de pesquisa que serão aprofundadas conforme as comparações avancem:

- **Estrutura e dados:** identificar como as duas edições organizam seus recursos e quais diferenças podem ser explicadas tecnicamente.
- **Equipes e modos:** comparar informações, opções e elementos de apresentação sem descaracterizar a edição americana.
- **Gráficos e textos:** localizar possíveis diferenças visuais e avaliar a viabilidade de recuperar recursos.
- **Narração e efeitos sonoros:** investigar especialmente as diferenças de áudio, uma das áreas de maior interesse do projeto.
- **Compatibilidade:** testar as mudanças em emuladores e, quando a base estiver estável, preparar verificações em hardware real.

Nenhum conteúdo será considerado restaurado apenas por ter sido localizado na outra ROM. Cada recurso precisará ser analisado, adaptado quando necessário e testado dentro da estrutura americana.

## Preservar primeiro, modificar com responsabilidade

As ROMs originais serão mantidas intactas. O desenvolvimento será feito em cópias de trabalho, com registro das alterações e atenção à compatibilidade. Essa postura permite comparar resultados, identificar problemas e voltar atrás quando uma experiência não produzir o comportamento esperado.

Também não queremos transformar esta primeira edição em uma expansão de conteúdo. Novas equipes, músicas ou reformulações visuais pertencem a possibilidades futuras e não fazem parte do objetivo imediato da American Restored Edition. O foco agora é construir uma restauração consistente do jogo que serviu de base ao projeto.

## Acompanhe o desenvolvimento

Este é o início de um trabalho de preservação e investigação técnica. Ainda há comparações a realizar, recursos a compreender e testes a executar. Por isso, o projeto não promete antecipadamente que todo conteúdo da edição japonesa poderá ser transferido: cada possibilidade dependerá dos resultados técnicos.

Acompanhe o andamento, as etapas e os indicadores na página do projeto:

**[ISS Deluxe – American Restored Edition: página do projeto](/covil-secreto/projetos/iss-deluxe-american-restored-edition/)**

*International Superstar Soccer Deluxe é uma obra de seus respectivos titulares. Este projeto é uma iniciativa independente de estudo e preservação, sem vínculo oficial com a Konami.*
