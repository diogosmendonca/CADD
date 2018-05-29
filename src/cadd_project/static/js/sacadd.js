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

  // *************************//
  // Declaração das Variáveis //
  // *************************//

  var codigoDisciplinaTemp;         // Variável temporária;
  var horaInicioTemp;               // Variável temporária;
  var horaTerminoTemp;              // Variável temporária;
  var i;                            // Variável temporária;
  var codigoDisciplina;             // Código da Disciplina que vem escrito nos detalhes completos da disciplina;
  var horaInicio;                   // Hora de Início da aula  que vem escrito nos detalhes completos da disciplina;
  var horaTermino;                  // Hora de Término da aula  que vem escrito nos detalhes completos da disciplina;
  var idDisciplinaCardBody;         // ID do CardBody que define as três primeiras letras iniciais do dia da semana
                                    // e é utilizada para definir para qual coluna a disciplina será enviada;
  var horaInicioTextoPlanoSemPontos;// Representa a hora de início da aula de forma concatenada e sem os dois pontos;
  var tempoDeAulaEmMinutos;         // Conversão do tempo total de aula para minutos;
  var celulaDestino;                // Célula de Destino da disciplina;
  var disciplinaDivObject;          // DIV com a disciplina;
  var countTemposAula;              //

  // ************************//
  // Definição das Variáveis //
  // ************************//

  idDisciplinaTemp = e.target.parentNode.getElementsByClassName("disciplina-previa-id");
  codigoDisciplinaTemp = e.target.parentNode.getElementsByClassName("disciplina-previa-desc");
//  codigoDisciplinaTemp = e.target.parentNode.getElementsByClassName("disciplina-previa-desc");
  horaInicioTemp  = e.target.parentNode.getElementsByClassName("disciplina-previa-horario-inicio");
  horaTerminoTemp = e.target.parentNode.getElementsByClassName("disciplina-previa-horario-termino");
  idDisciplinaCardBody = e.target.parentNode.parentNode.getAttribute("id");

  idDisciplina = idDisciplinaTemp[0].innerHTML;
  codigoDisciplina = codigoDisciplinaTemp[0].innerHTML;
  horaInicio = horaInicioTemp[0].innerHTML;
  horaTermino = horaTerminoTemp[0].innerHTML;

  if(!horaInicio){
    prepararDisciplinaSemHorario(document.getElementById(codigoDisciplina));
    moverDisciplina(document.getElementById(codigoDisciplina), "disciplinas-sem-horario");
    document.getElementById('disciplinas').value += idDisciplina + "_";
    return 0;
  }

  horaInicioTextoPlanoSemPontos = horaInicio.split(":");
  horaInicioTextoPlanoSemPontos = horaInicioTextoPlanoSemPontos[0]+horaInicioTextoPlanoSemPontos[1];
  horaInicioTextoPlanoSemPontosCopia = horaInicioTextoPlanoSemPontos;

  tempoDeAulaEmMinutos = Number(horaToMinutos(horaTermino)) - Number(horaToMinutos(horaInicio));
  celulaDestino = String(idDisciplinaCardBody+horaInicioTextoPlanoSemPontos);
  disciplinaDivObject = document.getElementById(codigoDisciplina);
  countTemposAula = (Number(tempoDeAulaEmMinutos)/Number(50));

  if (tempoDeAulaEmMinutos == Number(50)) {
    if (verificarConflito(celulaDestino, idDisciplinaCardBody, countTemposAula)) {
      alert("Não é possível incluir esta disciplina em seu plano de estudos pois a mesma está apresentando conflito de horário com outra disciplina já adicionada ao plano.");
    }
    else{
      prepararTabela(disciplinaDivObject, celulaDestino, countTemposAula);
      prepararDisciplina(disciplinaDivObject, celulaDestino);
      moverDisciplina(disciplinaDivObject, celulaDestino);
      document.getElementById('disciplinas').value += idDisciplina + "_";
    }
  }
  else{
    if (verificarConflito(celulaDestino, idDisciplinaCardBody, countTemposAula)) {
      alert("Não é possível incluir esta disciplina em seu plano de estudos pois a mesma está apresentando conflito de horário com outra disciplina já adicionada ao plano.");
    }
    else{
      prepararTabela(disciplinaDivObject, celulaDestino, countTemposAula);
      prepararDisciplina(disciplinaDivObject, celulaDestino);
      moverDisciplina(disciplinaDivObject, celulaDestino);
      document.getElementById('disciplinas').value += idDisciplina + "_";
    }
  }
}

function exibirDisciplinasSemHorario() {
  var x = document.getElementById('disciplinas-sem-horario');
  if (x.style.display === 'none') {
    x.style.display = 'block';
    } else {
    x.style.display = 'none';
  }
}

function prepararDisciplinaSemHorario(disciplinaDivObject){
  disciplinaDivObject.classList.remove("disciplina-previa");
  disciplinaDivObject.classList.add("disciplina-previa-sem-horario");
}

function verificarConflito(celulaDestino, idDisciplinaCardBody, countTemposAula){

  var CelulaDestino = document.getElementById(celulaDestino);
  var idDisciplinaCardBody;

  if(!verificarExistencia(celulaDestino)){
    return 1;
  }
  else{
    NextCellToVerify = celulaDestino.slice(3,7);
    NextCellToVerify = incrementarTempoEmHora(NextCellToVerify);
    var x = 0;
    x += CelulaDestino.innerHTML.length;
    for (i = 0; i < countTemposAula - 1; i++) {
      CellToVerify = String(idDisciplinaCardBody) + String(NextCellToVerify);
      CellToVerify = document.getElementById(CellToVerify);
      x += CellToVerify.innerHTML.length;
      NextCellToVerify = incrementarTempoEmHora(NextCellToVerify);
    }
    if(x){
      return(1);
    }
    else{
      return(0);
    }
  }
}

function verificarExistencia(celulaDestino){
  if(document.getElementById(celulaDestino)){
    return 1;
  }
  else{
    return 0;
  }
}

function prepararTabela(disciplinaDivObject, celulaDestino, countTemposAula){

  var CelulaDestino;
  var idDisciplinaCardBody = disciplinaDivObject.parentNode.id;

  CelulaDestino = document.getElementById(celulaDestino);
  CelulaDestino.rowSpan = countTemposAula;
  CelulaDestino.style.backgroundColor = "#CFC";
  CelulaDestino.style.border = "1px solid green";

  NextCellToDelete = celulaDestino.slice(3,7);
  NextCellToDelete = incrementarTempoEmHora(NextCellToDelete);

  for (i = 0; i < countTemposAula - 1; i++) {
    CellToDelete = String(idDisciplinaCardBody) + String(NextCellToDelete);
    CellToDelete = document.getElementById(CellToDelete);
    CellToDelete.parentNode.removeChild(CellToDelete);
    NextCellToDelete = incrementarTempoEmHora(NextCellToDelete);
  }
}

function incrementarTempoEmHora(hhmm){
  b = hhmm.slice(0,2);
  c = hhmm.slice(2,4);
  b = Number(b);
  c = Number(c);
  c += Number(50);
  if(c >= 60){
    b += Number(1);
    c -= Number(60);
  }
  b = String(b);
  c = String(c);
  if(c.length == 1){
    c = c + "0";
  }
  return (String(b)+(c));
}

function prepararDisciplina(disciplinaDivObject, celulaDestino){
  disciplinaDivObject.classList.remove("disciplina-previa");
  disciplinaDivObject.classList.add("disciplina-previa-tabela");
}

function horaToMinutos(hhmm){
  x = hhmm.split(":");
  y = x[0];
  z = x[1];
  y*=60;
  return  Number(y) + Number(z);
}

function moverDisciplina(disciplinaDivObject, celulaDestino){
  document.getElementById(celulaDestino).appendChild(disciplinaDivObject);
}

function removeDisciplina(e){
  var idDisciplinaTemp = e.target.parentNode.getElementsByClassName("disciplina-previa-desc");
  var idDisciplina = idDisciplinaTemp[0].innerHTML;
  var idCardBody = e.target.parentNode.parentNode.getAttribute("id");
  var idCardBody2 = idCardBody.slice(0,3);
  disciplinaDivObject = document.getElementById(idDisciplina);

  alert(idDisciplina + " " + idCardBody2);
  moverDisciplina(disciplinaDivObject,idCardBody2);
//  moverDisciplina2(idDisciplina,idCardBody,idCardBody2,2);
}
