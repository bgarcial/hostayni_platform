!function(i){i.fn.extend({slimScroll:function(e){var s=i.extend({width:"auto",height:"250px",size:"7px",color:"#000",position:"right",distance:"1px",start:"top",opacity:.4,alwaysVisible:!1,disableFadeOut:!1,railVisible:!1,railColor:"#333",railOpacity:.2,railDraggable:!0,railClass:"slimScrollRail",barClass:"slimScrollBar",wrapperClass:"slimScrollDiv",allowPageScroll:!1,wheelStep:20,touchScrollStep:200,borderRadius:"7px",railBorderRadius:"7px"},e);return this.each(function(){function o(e){if(h){var t=0;(e=e||window.event).wheelDelta&&(t=-e.wheelDelta/120),e.detail&&(t=e.detail/3),i(e.target||e.srcTarget||e.srcElement).closest("."+s.wrapperClass).is(m.parent())&&l(t,!0),e.preventDefault&&!v&&e.preventDefault(),v||(e.returnValue=!1)}}function l(i,e,t){v=!1;var o=m.outerHeight()-y.outerHeight();e&&(e=parseInt(y.css("top"))+i*parseInt(s.wheelStep)/100*y.outerHeight(),e=Math.min(Math.max(e,0),o),e=0<i?Math.ceil(e):Math.floor(e),y.css({top:e+"px"})),e=(b=parseInt(y.css("top"))/(m.outerHeight()-y.outerHeight()))*(m[0].scrollHeight-m.outerHeight()),t&&(e=i,i=e/m[0].scrollHeight*m.outerHeight(),i=Math.min(Math.max(i,0),o),y.css({top:i+"px"})),m.scrollTop(e),m.trigger("slimscrolling",~~e),r(),n()}function a(){g=Math.max(m.outerHeight()/m[0].scrollHeight*m.outerHeight(),30),y.css({height:g+"px"});var i=g==m.outerHeight()?"none":"block";y.css({display:i})}function r(){a(),clearTimeout(u),b==~~b?(v=s.allowPageScroll,f!=b&&m.trigger("slimscroll",0==~~b?"top":"bottom")):v=!1,f=b,g>=m.outerHeight()?v=!0:(y.stop(!0,!0).fadeIn("fast"),s.railVisible&&x.stop(!0,!0).fadeIn("fast"))}function n(){s.alwaysVisible||(u=setTimeout(function(){s.disableFadeOut&&h||c||p||(y.fadeOut("slow"),x.fadeOut("slow"))},1e3))}var h,c,p,u,d,g,b,f,v=!1,m=i(this);if(m.parent().hasClass(s.wrapperClass)){var w=m.scrollTop(),y=m.siblings("."+s.barClass),x=m.siblings("."+s.railClass);if(a(),i.isPlainObject(e)){if("height"in e&&"auto"==e.height){m.parent().css("height","auto"),m.css("height","auto");S=m.parent().parent().height();m.parent().css("height",S),m.css("height",S)}else"height"in e&&(S=e.height,m.parent().css("height",S),m.css("height",S));if("scrollTo"in e)w=parseInt(s.scrollTo);else if("scrollBy"in e)w+=parseInt(s.scrollBy);else if("destroy"in e)return y.remove(),x.remove(),void m.unwrap();l(w,!1,!0)}}else if(!(i.isPlainObject(e)&&"destroy"in e)){s.height="auto"==s.height?m.parent().height():s.height,w=i("<div></div>").addClass(s.wrapperClass).css({position:"relative",overflow:"hidden",width:s.width,height:s.height}),m.css({overflow:"hidden",width:s.width,height:s.height});var x=i("<div></div>").addClass(s.railClass).css({width:s.size,height:"100%",position:"absolute",top:0,display:s.alwaysVisible&&s.railVisible?"block":"none","border-radius":s.railBorderRadius,background:s.railColor,opacity:s.railOpacity,zIndex:90}),y=i("<div></div>").addClass(s.barClass).css({background:s.color,width:s.size,position:"absolute",top:0,opacity:s.opacity,display:s.alwaysVisible?"block":"none","border-radius":s.borderRadius,BorderRadius:s.borderRadius,MozBorderRadius:s.borderRadius,WebkitBorderRadius:s.borderRadius,zIndex:99}),S="right"==s.position?{right:s.distance}:{left:s.distance};x.css(S),y.css(S),m.wrap(w),m.parent().append(y),m.parent().append(x),s.railDraggable&&y.bind("mousedown",function(e){var s=i(document);return p=!0,t=parseFloat(y.css("top")),pageY=e.pageY,s.bind("mousemove.slimscroll",function(i){currTop=t+i.pageY-pageY,y.css("top",currTop),l(0,y.position().top,!1)}),s.bind("mouseup.slimscroll",function(i){p=!1,n(),s.unbind(".slimscroll")}),!1}).bind("selectstart.slimscroll",function(i){return i.stopPropagation(),i.preventDefault(),!1}),x.hover(function(){r()},function(){n()}),y.hover(function(){c=!0},function(){c=!1}),m.hover(function(){h=!0,r(),n()},function(){h=!1,n()}),m.bind("touchstart",function(i,e){i.originalEvent.touches.length&&(d=i.originalEvent.touches[0].pageY)}),m.bind("touchmove",function(i){v||i.originalEvent.preventDefault(),i.originalEvent.touches.length&&(l((d-i.originalEvent.touches[0].pageY)/s.touchScrollStep,!0),d=i.originalEvent.touches[0].pageY)}),a(),"bottom"===s.start?(y.css({top:m.outerHeight()-y.outerHeight()}),l(0,!0)):"top"!==s.start&&(l(i(s.start).position().top,null,!0),s.alwaysVisible||y.hide()),window.addEventListener?(this.addEventListener("DOMMouseScroll",o,!1),this.addEventListener("mousewheel",o,!1)):document.attachEvent("onmousewheel",o)}}),this}}),i.fn.extend({slimscroll:i.fn.slimScroll})}(jQuery),$(function(){$("#myPlaces-result").slimScroll({height:"180px",position:"right",railVisible:!0,alwaysVisible:!0,railOpacity:.1}),$("#map-results").slimScroll({height:"180px",position:"right",railVisible:!0,alwaysVisible:!0,railOpacity:.1});var i={height:"300px",position:"right",railVisible:!0,alwaysVisible:!1,railOpacity:.1};$("#blog-scroll").slimScroll(i)});