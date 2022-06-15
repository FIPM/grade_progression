
$('nav ul li').click(function(){
  $(this).addClass("active").siblings().removeClass("active");
});
$('.btn-layout').click(function(){
    $(this).toggleClass("click");
    $('.sidebar').toggleClass("show");
  });

/* as many as many submenus in menu*/
/* I guess I wont have more than 10 submenus*/
$('.F1-btn').click(function(){
      $('nav ul .F1-show').toggleClass("show1");
      $('nav ul .F1').toggleClass("rotate");      
    });
$('.F2-btn').click(function(){
      $('nav ul .F2-show').toggleClass("show2");
      $('nav ul .F2').toggleClass("rotate");
    });
$('.F3-btn').click(function(){
      $('nav ul .F3-show').toggleClass("show3");
      $('nav ul .F3').toggleClass("rotate");
    });
$('.F4-btn').click(function(){
      $('nav ul .F4-show').toggleClass("show4");
      $('nav ul .F4').toggleClass("rotate");
    });        
$('.F5-btn').click(function(){
      $('nav ul .F5-show').toggleClass("show5");
      $('nav ul .F5').toggleClass("rotate");
    });        
$('.F6-btn').click(function(){
      $('nav ul .F6-show').toggleClass("show6");
      $('nav ul .F6').toggleClass("rotate");
    });        
$('.F7-btn').click(function(){
      $('nav ul .F7-show').toggleClass("show7");
      $('nav ul .F7').toggleClass("rotate");
    });        
$('.F8-btn').click(function(){
      $('nav ul .F8-show').toggleClass("show8");
      $('nav ul .F8').toggleClass("rotate");
    });        
$('.F9-btn').click(function(){
      $('nav ul .F9-show').toggleClass("show9");
      $('nav ul .F9').toggleClass("rotate");
    });        
$('.F10-btn').click(function(){
      $('nav ul .F10-show').toggleClass("show10");
      $('nav ul .F10').toggleClass("rotate");
    });            


/* as many as many submenus in menu*/    
