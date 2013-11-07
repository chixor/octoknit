// Request Animation Frame Shim courtesy of Paul Irish & Jerome Etienne
(function() {
    var lastTime = 0;
    var vendors = ['webkit', 'moz'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame =
          window[vendors[x]+'CancelAnimationFrame'] || window[vendors[x]+'CancelRequestAnimationFrame'];
    }

    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); },
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };

    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());

// JClass -> JQuery plugin Bridge courtesy of Scott Gonzalez
(function() {
	$.plugin = function(name, object) {
		$.fn[name] = function(options) {
			var args = Array.prototype.slice.call(arguments, 1);
			return this.each(function() {
				var instance = $.data(this, name);
				if(instance) {
					instance[options].apply(instance, args);
				} else {
					instance = $.data(this, name, new object(options, this));
				}
			});
		};
	};
})();

/*!
 * JavaScript Inheritance with Private Members
 * Largely based upon John Resig's inheritance technique,
 * (see http://ejohn.org/blog/simple-javascript-inheritance/)
 * that was inspired by base2 and Prototype.
 *
 * Works with and without node.
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license
 *
 * v2.0.5, Marcel Rieger, 2013
 * https://github.com/riga/jclass
 * https://npmjs.org/package/jclass
 */
var ns,nsKey;
if(typeof global!=="undefined"&&typeof process!=="undefined"&&typeof module!=="undefined"&&module.exports){ns=module;nsKey="exports";}else{if(typeof window!=="undefined"){ns=window;
nsKey="JClass";}}(function(d,f){var b=d[f];var a={extendable:true,ctorName:"init",superName:"_super",enablePrivacy:true,privatePattern:/^__.+/,tracking:true,privateName:"__",methodsKey:"_jcMethods_",depthKey:"_jcDepth_",callerDepthKey:"_jcCallerDepth_"};
var c=false;var e=function(){};e.extend=function(m,g){g=g||{};for(var q in a){if(g[q]===undefined){g[q]=a[q];}}if(!g.enablePrivacy){g.privatePattern=null;
g.privateName=null;}var r=this.prototype;c=true;var o=new this();c=false;o[g.depthKey]=r[g.depthKey]||0;o[g.depthKey]++;var k=o[g.depthKey];var i={};var j={};
var s={};for(var h in m){if(m[h] instanceof Function){var n=(function(t,u){return function(){var v=this[g.superName];if(!g.privatePattern||!g.privatePattern.test(t)){this[g.superName]=r[t];
}var D;if(g.privateName){D=this[g.privateName];this[g.privateName]=D||s;}var y,E,x,I;if(g.privatePattern){if(this[g.callerDepthKey]===undefined){this[g.callerDepthKey]=k;
}y=this[g.methodsKey];if(t==g.ctor){this[g.methodsKey]=y||i;for(var z in i){if(!this[g.methodsKey][z]){this[g.methodsKey][z]={};}this[g.methodsKey][z][k]=i[z][k];
var C=this[g.methodsKey][z][k];this[g.methodsKey][z][k]=function(){var K=this[g.superName];this[g.superName]=this[g.methodsKey][z][k-1];var J=C.apply(this,arguments);
this[g.superName]=K;return J;};}i=this[g.methodsKey];}else{this[g.methodsKey]=i;}E={};for(var z in this[g.methodsKey]){E[z]=this[z];var F=Math.max.apply(Math,Object.keys(i[z]));
this[z]=i[z][F];}if(g.tracking){x={};for(var G in j){x[G]=this[G];this[G]=j[G];}}if(g.tracking){I=Object.keys(this);}}var B=u.apply(this,arguments);if(g.privatePattern){if(g.tracking){var H=Object.keys(this);
for(var G in H){G=H[G];if(g.privatePattern.test(G)){x[G]=this[G];j[G]=this[G];}}for(var G in I){G=I[G];var A=H.indexOf(G)<0&&g.privatePattern.test(G);if(A){delete j[G];
delete this[G];}}for(var G in j){var w=this[g.callerDepthKey];if(x[G]===undefined||k==w){delete this[G];}else{this[G]=x[G];}}}for(var G in this[g.methodsKey]){if(E[G]===undefined){delete this[G];
}else{this[G]=E[G];}}if(y===undefined){delete this[g.methodsKey];}else{this[g.methodsKey]=y;}if(k==this[g.callerDepthKey]){delete this[g.callerDepthKey];
}}if(g.privateName){if(D===undefined){delete this[g.privateName];}else{this[g.privateName]=D;}}if(v===undefined){delete this[g.superName];}else{this[g.superName]=v;
}return B;};})(h,m[h]);var l=g.privatePattern&&g.privatePattern.test(h);if(l){i[h]={};i[h][k]=n;}else{o[h]=n;}}else{var l=g.tracking&&g.privatePattern&&g.privatePattern.test(h);
if(l){j[h]=m[h];}else{o[h]=m[h];}}}function p(){if(!c&&this[g.ctorName]){this[g.ctorName].apply(this,arguments);}}p.prototype=o;p.prototype.constructor=p;
if(g.extendable!==false){p.extend=arguments.callee;}return p;};e.noConflict=function(){var g=d[f];d[f]=b;return g;};d[f]=e;})(ns,nsKey);

/*
 * Animations on the icons
 */
var SlideMagic = JClass.extend({
	defaults : {
		animate: true,
		primaryColor: '#000',
		secondaryColor: '#fff',
		font: 'HelveticaNeue-UltraLight',
	},
	init : function(options, element) {
		this.defaults.animate = !$('html').hasClass('ieLegacy');
		this.options = $.extend(true, {}, this.defaults, options);
		this.$el = $(element);

		// frame rate stuff
		this.timing = {};
		this.timing.fps = 30;
		this.timing.now;
		this.timing.then = Date.now();
		this.timing.interval = 1000/this.timing.fps;
		this.timing.delta;

		// setup context and animation variables
		this.options.ctx = this.$el[0].getContext("2d");
		this.resize();
		this.pause = false;
		this.animating = false;

		// attach events
		this.bindEvents();
			
		// animation stuff
		if(this.setup) this.setup();
		(this.options.animate) ? this.frame = 0 : this.frame = this.totalFrames;
		this.initalRender = true;
		this.render();
		this.initalRender = false;
		
		return element;
	},
	bindEvents : function() {
		this.$el.bind('startAnimation', {context: this}, function(event) {
			event.data.context.beginAnimation();
		});
		$(window).bind('pauseAnimation', {context: this}, function(event) {
			event.data.context.pauseAnimation();
		});
		$(window).bind('resetAnimation', {context: this}, function(event) {
			event.data.context.reset();
		});
		$(window).bind('resize', {context: this}, function(event) {
			event.data.context.resize();
		});
		this.$el.bind('animationRedrawLastFrame', {context: this}, function(event) {
			event.data.context.redraw();
		});

		// respond to mouse / touch events
		this.$el.bind('mousemove.hover', {context: this}, function(event) {
			event.data.context.hover(event);
		});
		if(this.click != undefined) {
			this.$el.bind('click', {context: this}, function(event) {
				event.data.context.click(event);
			});	
			this.$el.bind('touchend', {context: this}, function(event) {
				event.data.context.click(event);
			});
		}
	},
	hover : function(e) {
		if(this.hotspots != undefined && !this.animating) {
			(this.findTarget(event.pageX, 0, event.pageY, this.$el[0].offsetTop) > -1) ? 
				this.$el.css('cursor','pointer') :
				this.$el.css('cursor','default');
		}
	},
	findTarget : function(pointX, offsetX, pointY, offsetY) {
		// these animations are predominently centered in the page so we need to take the X coord from the offset of the center
		pointX = (this.$el.width()/2) - (($(window).width()/2) - pointX);

		for(var spot = 0; spot < this.hotspots.length; spot++) {
            if(pointX < this.hotspots[spot].centerx + this.hotspots[spot].distance + offsetX 
            && pointX > this.hotspots[spot].centerx - this.hotspots[spot].distance + offsetX 
            && pointY < this.hotspots[spot].centery + this.hotspots[spot].distance + offsetY 
            && pointY > this.hotspots[spot].centery - this.hotspots[spot].distance + offsetY) {
            	this.target = spot;
				return this.target;
            }
        }
        this.target = -1;
        return this.target;
	},
	resize : function() {
		if($(window).width() <= 400) {
			this.$el.width($(window).width()*0.5).height($(window).width()*0.5);
		} else if(this.$el.width() < 290) {
			this.$el.removeAttr('style');
		}
		if(!this.options.animate) { 
			this.frame = this.totalFrames;
		}
		this.animate();
	},
	reset : function() {
		// only reset if we reached the end of the animation
		if(this.totalFrames - this.frame < 10) {
			this.frame = 0;
			this.pause = false;
			this.render();
		}
	},
	render : function() {
		this.draw();
		this.drawFrame();
	},
	beginAnimation : function() {
		this.pause = false;
		this.animating = true;
		this.configure();
		if(!this.options.animate) this.frame = this.totalFrames;
		this.animate();
	},
	animate : function() {
	    this.timing.now = Date.now();
	    this.timing.delta = this.timing.now - this.timing.then;
     
	    if (this.timing.delta > this.timing.interval) {
 			this.frame++;
 			this.timing.then = this.timing.now - (this.timing.delta % this.timing.interval);
 			if(this.options.buildReverse) {
				this.drawFrame();
		 		this.draw();
			} else {
		 		this.draw();
				this.drawFrame();
			}
		}
		this.trigger();
	},
	redraw : function() {
		if(!this.animating) {
			if(this.options.buildReverse) {
				this.drawFrame();
				this.draw();
			} else {
				this.draw();
				this.drawFrame();
			}
		}
	},
	pauseAnimation : function() {
		this.pause = true;
	},
	easeIn : function(startingOffset, thisFrame, totalFrames, totalDifference, velocity) {
		var t = thisFrame, b = startingOffset, c = totalDifference, d = totalFrames, v = velocity;
		return c * (( t = t / d - 1) * t * ((v + 1) * t + v) + 1) + b;
	},
	easeOutQuad : function(t, b, c, d) {
		t /= d;
		return -c * t*(t-2) + b;
	},
	trigger : function() {
		if(this.pause) return;

		if (this.frame < this.totalFrames) {
			var elem = this;
			//setTimeout(function() {
				requestAnimationFrame(elem.animate.bind(elem));
			//}, 1000 / 30);
		} else {
			this.animating = false;
		}
	},
	wrapText : function(text, x, y, maxWidth, lineHeight, fontSize) {
		var ctx = this.options.ctx, words = [];
		// to take an accurate measurement we need the context font setup correctly
		ctx.font=fontSize+"px "+this.options.font;

		if(typeof text === 'string')
			words.push(text.split(' '));
		else if(typeof text === 'object') {
			// an array will always line break at the end of each array element
			for(var w = 0; w < text.length; w++)
				if(text[w] != null && text[w] != '')
					words.push(text[w].split(' '));
		}

        var line = '', lines = [], totalHeight = -(fontSize*0.5), tail = false, leftover = Math.floor(ctx.measureText(' ').width/2), workingLineHeight = lineHeight*fontSize, testLine, metrics, testWidth;

        for(var w = 0; w < words.length; w++) {
	        for(var n = 0; n < words[w].length; n++) {
	          testLine = line + words[w][n] + ' ';
	          testWidth = ctx.measureText(testLine).width;
	          
	         	// if we've met the limit, push the buffer
	        	if (testWidth > maxWidth) {
	        		// push the shorter line if it's not empty
	        		if(line != '') {
						if(lines.length > 0) {
							y += workingLineHeight;
							totalHeight += workingLineHeight;
						}
	        			lines.push(new Array(line, x+leftover, y, fontSize, workingLineHeight));
	        			workingLineHeight = lineHeight*fontSize;
					}

					// if the single word was too long, push that as well
					var wordWidth = ctx.measureText(words[w][n]+' ').width;
					if(wordWidth > maxWidth) {
						// scale the font so it fits
						var newFS = Math.floor(fontSize*(maxWidth/wordWidth));
		        		workingLineHeight = lineHeight*(fontSize);
						
						if(lines.length > 0) {
							y += workingLineHeight;
							totalHeight += workingLineHeight;
						}
		        		lines.push(new Array(words[w][n]+' ', x+leftover, y, newFS, workingLineHeight));
		        		line = '';
		        		workingLineHeight = lineHeight*(fontSize);
		        		tail = false;
		        	} 
		        	// otherwise build the buffer
		        	else {
		        		line = words[w][n]+' ';
		        		tail = true;
		        	}
	        	} 
	        	// otherwise build the buffer
	        	else {
	        		line = testLine;
	        		tail = true;
	        	}
	        }
	        if(tail) {
	        	if(lines.length > 0) {
			        y += workingLineHeight;
			        totalHeight += workingLineHeight;
			    }
		        lines.push(new Array(line, x+leftover, y, fontSize, workingLineHeight));
		        workingLineHeight = lineHeight*fontSize;
	        	line = '';
        	}
        }
        
        // amend vertical offset based on number of lines we have to output
        for(var x = 0; x < lines.length; x++) {
        	lines[x][2] = Math.floor(lines[x][2]-(totalHeight/2));
		}

        return lines;
	},
	cacheText : function(lines,size) {
		var canvas = document.createElement( 'canvas' );
		canvas.width = size;
		canvas.height = size;

		var ctx = canvas.getContext( '2d' );
		ctx.textAlign = 'center';
	    ctx.fillStyle = this.options.primaryColor;

		for(var w = 0; w < lines.length; w++) {
			ctx.font=lines[w][3]+"px "+this.options.font;
			ctx.fillText(lines[w][0], (size/2)+lines[w][1], (size/2)+lines[w][2]);
		}
	
		return canvas;
	}
});

var SlideMagicSpiral = SlideMagic.extend({
	defaults : {
		a: 2,
		b: 22.2,
		buildReverse: true,
		primaryColor: '#000',
		secondaryColor: '#fff',
		font: 'HelveticaNeue-UltraLight'
	},
	click : function(e) {
		e.stopPropagation();
		e.preventDefault();

		console.log('trigger!');
	},
	configure : function() {
		this.totalFrames = 145;
	},
	draw : function() {
		var ctx = this.options.ctx;
		var centerx = this.$el[0].width / 2;
		var centery = this.$el[0].height / 2;

		var scale = 20, height = scale*0.625, voffset = 0, angle = scale*0.32;
		for(var w = 0; w < (this.$el[0].height/height); w++) {
			for(var x = 0; x < (this.$el[0].width/scale); x++) {
				ctx.beginPath();
				ctx.moveTo((x*scale),voffset);
				ctx.lineTo((x*scale),voffset+height);
				ctx.lineTo(((x*scale)+(scale/2)),voffset+height+angle);
				ctx.lineTo((x*scale)+scale,voffset+height);
				ctx.lineTo((x*scale)+scale,voffset);
				ctx.lineTo((x*scale)+(scale/2),voffset+angle);
				ctx.lineTo((x*scale),voffset);

				ctx.moveTo((x*scale)+(scale/2),voffset+angle);
				ctx.lineTo(((x*scale)+(scale/2)),voffset+height+angle);

			    ctx.strokeStyle = this.options.primaryColor;
				ctx.lineWidth = 0.5;
			    ctx.stroke();
			    
			    if((w % x < 2) || (w % x > 9)) {
			    	ctx.fillStyle = this.options.primaryColor;
			    	ctx.fill();
				}
			    
				ctx.closePath();
			}
			voffset = voffset+height;
		}
	},
	drawFrame : function() {
		var ctx = this.options.ctx;
	}
});

// setup drawing objects as jquery plugins
$.plugin('SlideMagicSpiral', SlideMagicSpiral);

/*
 * Initialization code
 */
$(window).load(function() {
	var options = {animate: !$('html').hasClass('ieLegacy')};
	$('canvas').SlideMagicSpiral($.extend({},options,{}));
	//$('canvas').trigger('startAnimation');
});