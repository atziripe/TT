var marcha=0; //control del temporizador
var cro=0; 
visor=document.getElementById("reloj");
//Botón 1: Estado empezar: Poner en marcha el crono
function empezar() {
    emp=new Date(); //fecha inicial (en el momento de pulsar)
    elcrono=setInterval(tiempo,10); //poner en marcha el temporizador.
    marcha=1; //indicamos que se ha puesto en marcha.
}

//función del temporizador	
function tiempo() { 
    actual=new Date(); //fecha a cada instante	
       //tiempo del crono (cro) = fecha instante (actual) - fecha inicial (emp)	
    cro=actual-emp; //milisegundos transcurridos.	
    cr=new Date(); //pasamos el num. de milisegundos a objeto fecha.	
    cr.setTime(cro); 
       //obtener los distintos formatos de la fecha:	
    cs=cr.getMilliseconds(); //milisegundos 	
    cs=cs/10; //paso a centésimas de segundo.	
    cs=Math.round(cs); //redondear las centésimas	
    sg=cr.getSeconds(); //segundos 	
    mn=cr.getMinutes(); //minutos 	
       //poner siempre 2 cifras en los números			 
    if (cs<10) {cs="0"+cs;} 
    if (sg<10) {sg="0"+sg;} 
    if (mn<10) {mn="0"+mn;} 
       //llevar resultado al visor.			 
    visor.innerHTML=mn+" "+sg+" "+cs; 
    if (visor.innerHTML == "00 24 00"){
        clearInterval(elcrono);
        marcha = 0;
    }
}


//Continuar una cuenta empezada y parada.
function continuar() {
    emp2=new Date(); //fecha actual
    emp2=emp2.getTime(); //pasar a tiempo Unix
    emp3=emp2-cro; //restar tiempo anterior
    emp=new Date(); //nueva fecha inicial para pasar al temporizador 
    emp.setTime(emp3); //datos para nueva fecha inicial.
    elcrono=setInterval(tiempo,10); //activar temporizador
    marcha=1; //indicar que esta en marcha
}

//parar el cronómetro
function catchtime() { 
    clearInterval(elcrono); //parar el crono
    marcha=0; //indicar que está parado.
    const timeword = visor.innerHTML;
    continuar()
    return timeword;
}	
