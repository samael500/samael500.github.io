(function(){var a;a=function(c,d){var b;this.$el=c;this.direction=(b=d.direction)!=="vertical"&&b!=="horizontal"?"vertical":d.direction;this.src=d.src;this.timeoutValue=d.timeout!=null?d.timeout:500;this.timeoutId=0;this.initDelay=d.initDelay!=null?d.initDelay:true;this.$el.addClass("wbt-comparator wbt-comparator__"+this.direction);this.loadedImages=0;this.isInitialized=false;this.imagesLoad();if(this.initDelay){return $(window).on("scroll",{"this":this},this.imagesInitIfVisible)}};a.prototype.imagesLoad=function(){var e,i,d,h,g,c,f,b;d=this;f=this.src;b=[];for(i=g=0,c=f.length;g<c;i=++g){h=f[i];e=$(new Image());this.$el.append(e);e.addClass("wbt-comparator_image");if(i===0){this.imageBackground=e.wrap("<div class='wbt-comparator_wrap wbt-comparator_wrap__background'>").parent()}else{this.imageOverlay=e.wrap("<div class='wbt-comparator_wrap wbt-comparator_wrap__overlay'>").parent()}e.on("load",function(){if(++d.loadedImages===2){if(d.initDelay){d.imagesInitIfVisible({data:{"this":d}})}else{d.imagesInit()}}return d.imageOverlay.css({height:d.imageBackground.height(),width:d.imageBackground.width()})});b.push(e.attr({src:h}))}return b};a.prototype.imagesInit=function(){var b;b=this;this.isInitialized=true;this.imageOverlay.addClass("wbt-comparator_reset__"+this.direction);this.$el.on("mousemove touchmove",function(d){var c,f;d.preventDefault();clearTimeout(b.timeoutId);b.imageOverlay.removeClass("wbt-comparator_reset__"+b.direction);f=b.imageBackground.offset();c=d.type==="touchmove"?d.originalEvent.touches[0]:d;if(b.direction==="horizontal"){return b.imageOverlay.css("width",c.pageX-f.left)}else{return b.imageOverlay.css("height",c.pageY-f.top)}});if(this.timeoutValue!==false){return this.$el.on("mouseleave touchend",function(){return b.timeoutId=setTimeout(function(){return b.imageOverlay.addClass("wbt-comparator_reset__"+b.direction)},b.timeoutValue)})}};a.prototype.imagesInitIfVisible=function(d){var c,b;b=d.data["this"];if(b.isInitialized){return}c=b.$el[0].getBoundingClientRect();if(c.top>=0&&c.top<=$(window).height()||c.bottom>=0&&c.bottom<=$(window).height()){return b.imagesInit()}};$.fn.wbtComparator=function(b){return new a(this,b)}}).call(this);