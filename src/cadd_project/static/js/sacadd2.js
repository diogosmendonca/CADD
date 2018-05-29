/*!
  * Sistema de Apoio às CADDs
  * Copyright 2018
  */

// para o form plano de estudos e plano de estudos cadastrados
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text/html", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text/html");
  ev.target.appendChild(document.getElementById(data));
}


// para o form plano de estudos prévia
function addDisciplina(e){
  var codigoTemp = e.target.parentNode.getElementsByClassName("disciplina-previa-desc");
  var horarioInicioTemp  = e.target.parentNode.getElementsByClassName("disciplina-previa-horario-inicio");
  var horarioTerminoTemp = e.target.parentNode.getElementsByClassName("disciplina-previa-horario-termino");
  var i;
  var codigoDisciplina;
  var horarioInicio;
  var horarioTermino;

  for (i = 0; i < codigoTemp.length; i++) {
    codigoDisciplina = codigoTemp[i].innerHTML;
  }
  for (i = 0; i < horarioInicioTemp.length; i++) {
    horarioInicio = horarioInicioTemp[i].innerHTML;
  }
  for (i = 0; i < horarioTerminoTemp.length; i++) {
    horarioTermino = horarioTerminoTemp[i].innerHTML;
  }

  var idCardBody = e.target.parentNode.parentNode.getAttribute("id");

  if (idCardBody == "out") {
    blocoHorario = "00";
    tempoAula = Number(50);
  }else{
    blocoHorario = horarioInicio.split(":");
    blocoHorario = blocoHorario[0]+blocoHorario[1];
    tempoAula = Number(horaToMinutos(horarioTermino)) - Number(horaToMinutos(horarioInicio));
  }
  blocoHorario2 = blocoHorario;

  if (tempoAula == Number(50)) {
    blocoHorario = idCardBody+blocoHorario;
    moverDisciplina(codigoDisciplina,blocoHorario,1);
//    moverDisciplina2(codigoDisciplina,idCardBody,blocoHorario,1);
  }else{
    blocoHorario = idCardBody+blocoHorario;
    prepararTabela(blocoHorario2,tempoAula,idCardBody);
    moverDisciplina(codigoDisciplina,blocoHorario,1);
//    moverDisciplina2(codigoDisciplina,idCardBody,blocoHorario,1);
    prepararDisciplina(blocoHorario2,idCardBody);
  }
}

function prepararTabela(localizacaoDesejada,tempoAula,idCardBody){
  var celulaDestino = String(idCardBody) + String(localizacaoDesejada);
  var countTemposAula = (Number(tempoAula)/50);
  // celulaDestino.rowSpan = String(countTemposAula);
  // document.getElementById(celulaDestino).rowSpan = String(countTemposAula)
}

function prepararDisciplina(localizacaoDesejada,idCardBody){
  var celulaDestino = String(idCardBody) + String(localizacaoDesejada);
  temp = document.getElementById(celulaDestino);
  temp.Style.backgroundColor ="red";
}

function removeDisciplina(e){
  var idDisciplinaTemp = e.target.parentNode.getElementsByClassName("disciplina-previa-desc");
  var i;
  for (i = 0; i < idDisciplinaTemp.length; i++) {
    idDisciplina = idDisciplinaTemp[i].innerHTML;
  }
  var idCardBody = e.target.parentNode.parentNode.getAttribute("id");
  var idCardBody2 = idCardBody.slice(0,3);
  moverDisciplina(idDisciplina,idCardBody2,2);
//  moverDisciplina2(idDisciplina,idCardBody,idCardBody2,2);
}

function horaToMinutos(tempo){
  x = tempo.split(":");
  y = x[0];
  z = x[1];
  y*=60;
  return  Number(y) + Number(z);
}

function moverDisciplina(idDisciplina, idLocalizacaoNova, tipoMovimento){
  if (tipoMovimento == 1) {
    if (!document.getElementById(idLocalizacaoNova).hasChildNodes()) {
      document.getElementById(idLocalizacaoNova).appendChild(document.getElementById(idDisciplina));
      document.querySelector('input[id="chk"+idLocalizacaoNova]').checked;
      document.getElementById("chk"+idLocalizacaoNova).checked;
    }
  }else{
    document.getElementById(idLocalizacaoNova).appendChild(document.getElementById(idDisciplina));
  }
}

function moverDisciplina2(idDisciplina, idLocalizacaoAntiga, idLocalizacaoNova, tipoMovimento){
  var localAntigo = document.getElementById(idLocalizacaoAntiga);
  var localNovo = document.getElementById(idLocalizacaoNova);
  var no = document.getElementById(idDisciplina);
  var objeto;

  if (tipoMovimento == 1) {
    if (!localNovo.hasChildNodes()) {
      objeto = localAntigo.removeChild(no);
      localNovo.appendChild(objeto);
    }
  }else{
    objeto = localAntigo.removeChild(no);
    localNovo.appendChild(objeto);
  }
}
