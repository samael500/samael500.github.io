// Generated by CoffeeScript 1.7.1

/*
* wbt.comparator.js v1.0.0
*
* Licensed under the MIT license.
* http://opensource.org/licenses/mit-license.php
*
* Dependencies: jQuery 1.7+
*
* Basic usage:
* $(".any-selector").wbtComparator({
*   src: [
      "path/to/first/image.jpg",
      "path/to/second/image.jpg"
    ]
* });
*
* For more instructions and examples, please visit http://wbtech.pro/blog/comparator/
*
* Copyright 2014, WBTech
* http://wbtech.pro/
 */

(function() {
  var WBTComparator;

  WBTComparator = function($this, params) {
    var _ref;
    this.$el = $this;
    this.direction = (_ref = params.direction) !== "vertical" && _ref !== "horizontal" ? "vertical" : params.direction;
    this.src = params.src;
    this.timeoutValue = params.timeout != null ? params.timeout : 500;
    this.timeoutId = 0;
    this.initDelay = params.initDelay != null ? params.initDelay : true;
    this.$el.addClass("wbt-comparator wbt-comparator__" + this.direction);
    this.loadedImages = 0;
    this.isInitialized = false;
    this.imagesLoad();
    if (this.initDelay) {
      return $(window).on("scroll", {
        "this": this
      }, this.imagesInitIfVisible);
    }
  };

  WBTComparator.prototype.imagesLoad = function() {
    var $imageNew, id, self, source, _i, _len, _ref, _results;
    self = this;
    _ref = this.src;
    _results = [];
    for (id = _i = 0, _len = _ref.length; _i < _len; id = ++_i) {
      source = _ref[id];
      $imageNew = $(new Image());
      this.$el.append($imageNew);
      $imageNew.addClass("wbt-comparator_image");
      if (id === 0) {
        this.imageBackground = $imageNew.wrap("<div class='wbt-comparator_wrap wbt-comparator_wrap__background'>").parent();
      } else {
        this.imageOverlay = $imageNew.wrap("<div class='wbt-comparator_wrap wbt-comparator_wrap__overlay'>").parent();
      }
      $imageNew.on("load", function() {
        if (++self.loadedImages === 2) {
          if (self.initDelay) {
            self.imagesInitIfVisible({
              data: {
                "this": self
              }
            });
          } else {
            self.imagesInit();
          }
        }
        return self.imageOverlay.css({
          height: self.imageBackground.height(),
          width: self.imageBackground.width()
        });
      });
      _results.push($imageNew.attr({
        src: source
      }));
    }
    return _results;
  };

  WBTComparator.prototype.imagesInit = function() {
    var self;
    self = this;
    this.isInitialized = true;
    this.imageOverlay.addClass("wbt-comparator_reset__" + this.direction);
    this.$el.on("mousemove touchmove", function(e) {
      var event, offset;
      e.preventDefault();
      clearTimeout(self.timeoutId);
      self.imageOverlay.removeClass("wbt-comparator_reset__" + self.direction);
      offset = self.imageBackground.offset();
      event = e.type === "touchmove" ? e.originalEvent.touches[0] : e;
      if (self.direction === "horizontal") {
        return self.imageOverlay.css("width", event.pageX - offset.left);
      } else {
        return self.imageOverlay.css("height", event.pageY - offset.top);
      }
    });
    if (this.timeoutValue !== false) {
      return this.$el.on("mouseleave touchend", function() {
        return self.timeoutId = setTimeout(function() {
          return self.imageOverlay.addClass("wbt-comparator_reset__" + self.direction);
        }, self.timeoutValue);
      });
    }
  };

  WBTComparator.prototype.imagesInitIfVisible = function(e) {
    var rect, self;
    self = e.data["this"];
    if (self.isInitialized) {
      return;
    }
    rect = self.$el[0].getBoundingClientRect();
    if (rect.top >= 0 && rect.top <= $(window).height() || rect.bottom >= 0 && rect.bottom <= $(window).height()) {
      return self.imagesInit();
    }
  };

  $.fn.wbtComparator = function(params) {
    return new WBTComparator(this, params);
  };

}).call(this);