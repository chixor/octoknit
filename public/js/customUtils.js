// Request Animation Frame Shim courtesy of Paul Irish & Jerome Etienne
(function() {
    var lastTime = 0;
    var vendors = ['webkit', 'moz'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[needle]+'RequestAnimationFrame'];
        window.cancelAnimationFrame =
          window[vendors[needle]+'CancelAnimationFrame'] || window[vendors[needle]+'CancelRequestAnimationFrame'];
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
var StitchPattern = JClass.extend({
	init : function(options, element) {
		// setup variables
		//this.options = $.extend(true, {}, this.defaults, options);
		this.width = 936;
		this.height = 510;
		this.stageScale = 0.782;
		this.scale = 19.956;
		this.buildFormStarted = false;
		this.origin = {
			x: 0,
			y: 0
		}

		// prepare objects
		this.$el = $('#stitchCanvasContainer');
		this.stage = new Kinetic.Stage({
			container: this.$el.attr('id'),
			width: this.width,
			height: this.height,
			scale: this.stageScale,
			draggable: false
		});
		this.layer = new Kinetic.Layer();
		this.stitches = [];

		// build environment
		this.build();
		this.bindEvents();
		
		return element;
	},
	bindEvents : function() {
		var elem = this;
		$(this.stage.content).on('mousewheel', function(event) {
	        event.preventDefault();
			elem.zoom(event);
		});
		$('form#stitchpattern').bind('submit', function(e) {
			if(elem.buildFormStarted) return true;
			else return elem.buildForm(e);
		});
		$('#imageLoader').bind('change', function(e) {
			elem.loadFromImage(e.target.files[0]);
		});

		/* support drag and drop */
		this.$el.on('dragenter', function (e) 
		{
		    e.stopPropagation();
		    e.preventDefault();
		    $(this).css('border', '2px solid #0B85A1');
		});
		this.$el.on('dragover', function (e) 
		{
		     e.stopPropagation();
		     e.preventDefault();
		});
		this.$el.on('drop', function (e) 
		{
		     $(this).css('border', '2px dotted #0B85A1');
		     e.preventDefault();
		     var files = e.originalEvent.dataTransfer.files;
		 
		     elem.loadFromImage(files[0]);
		});
	},
	loadFromImage : function(file) {
        elem = this;
	    var reader = new FileReader();
	    reader.onload = function(event){
	        var img = new Image();
	        img.onload = function(){
				var canvas = document.createElement( 'canvas' );
				canvas.width = 60;
				canvas.height = 150;
				var ctx = canvas.getContext( '2d' );
				var imgwidth = canvas.width, imgheight = Math.round(canvas.width * img.height / img.width);
	            
	            ctx.drawImage(img,0,0);
				document.body.appendChild(canvas);
	            
	            // Get the CanvasPixelArray so we can iterate it
				var pix = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
				
				// Loop over each pixel and invert the color.
				var str = '';
				for (var i = 0, n = pix.length; i < n; i += 4) {
					(pix[i] < 100 && pix[i+1] < 100 && pix[i+2] < 100) ? str += '1' : str += '0';
				}

				$('input[name=stitches]').val(str);
				elem.build();
				elem.$el.css('border', '');
	        }
	        img.src = event.target.result;
	    }
	    reader.readAsDataURL(file);
	},
	buildForm : function(e) {
		if(!this.buildFormStarted) {
			this.buildFormStarted = true;

			var maxrows = 150, maxneedles = 60, data = '';
			for(var row = 0; row < maxrows; row++) {
				for(var needle = 0; needle < maxneedles; needle++) {
					(this.stitches[row][needle].poly.getFill() == 'white') ?
						data += '0':
						data += '1';
				}
			}
			$('input[name=stitches]').val(data);
			this.stage.toImage({
				callback : function(call) {
					//console.log('submitting...');
					$('input[name=preview]').val(call.src);
					$('input[type=submit]').trigger('click');
				}
			});
			return false;
		}
	},
	zoom : function(event) {
        var evt = event.originalEvent,
            mx = evt.clientX,
            my = evt.clientY,
            wheel = evt.wheelDelta / 120; //n or -n
        var zoom = (1.1 - (evt.wheelDelta < 0 ? 0.2 : 0));
        var newscale = this.stageScale * zoom;
        
        if(newscale > 0.3 && newscale < 2) {
	        this.origin.x = mx / this.stageScale + this.origin.x - mx / newscale;
	        this.origin.y = my / this.stageScale + this.origin.y - my / newscale;
	        this.stage.setOffset(this.origin.x, this.origin.y);
	        this.stage.setScale(newscale);
	        this.stage.draw();
	        this.stageScale *= zoom;
        }
	},
	build : function() {
		var maxrows = 150, 
			maxneedles = 60,
			height = this.scale*0.7, 
			voffset = 0-(maxrows*height)+this.height+110, 
			angle = this.scale*0.32,
			stitches = ($('input[name=stitches]').val() != undefined) ? $('input[name=stitches]').val() : null,
			count = 0;

		this.stage.destroyChildren();
		for(var row = 0; row < maxrows; row++) {
			this.stitches[row] = [];

			for(var needle = 0; needle < maxneedles; needle++) {
				this.stitches[row][needle] = {};

				this.stitches[row][needle].poly = new Kinetic.Polygon({
					points: [
						(needle*this.scale), 					voffset + height,
						((needle*this.scale) + (this.scale/2)), voffset + height + angle,
						(needle*this.scale) + this.scale, 		voffset + height,
						(needle*this.scale) + this.scale, 		voffset,
						(needle*this.scale) + (this.scale/2),	voffset + angle,
						(needle*this.scale),					voffset
					],
					fill: (stitches != null && stitches.charAt(count) == 0) ? 'white' : 'black',
					stroke: 'black',
					strokeWidth: 0.2
				});
				this.stitches[row][needle].poly.row = row;
				this.stitches[row][needle].poly.needle = needle;

				// attach events
				var elem = this;
				this.stitches[row][needle].poly.on('mousedown', function(e) {
					if(this.getFill() == 'white' && !elem.paint) {
						this.setFill('black');
						this.draw();
					} else {
						this.setFill('white');
						this.setStroke('white');
						this.draw();
						this.setStroke('black');
						this.draw();
					}
					elem.paint = true;
				});
				this.stitches[row][needle].poly.on('mousemove', function(e) {
					if(elem.paint) {
						this.setFill('black');
						this.draw();
					}
				});
				$(document).bind('mouseup', function(e) {
					elem.paint = false;
				});
		
				// add the shape to the layer
				this.layer.add(this.stitches[row][needle].poly);
				count++;
			}
			voffset = voffset+height;
		}
		
		this.layer.on('mouseenter', function() {
			elem.stage.setDraggable(false);
		});	
		this.layer.on('mouseleave', function() {
			elem.stage.setDraggable(true);
		});

		
		// draw the guidelines
		voffset = 0-(maxrows*height)+this.height+115;
		for(var needle = 5; needle < maxneedles; needle=needle+5) {
			var hr = new Kinetic.Line({
				points: [
					(needle*this.scale), voffset,
					(needle*this.scale), voffset+(height*maxrows)+10,
				],
				stroke: 'black',
				strokeWidth: 0.6
			});

			var labelTop = new Kinetic.Text({
				x: (needle*this.scale),
				y: voffset - 20,
				text: needle,
				fontSize: 20,
				fontFamily: 'Calibri',
				fill: 'black'
			});

			var labelBottom = new Kinetic.Text({
				x: (needle*this.scale), 
				y: voffset+(height*maxrows)+10,
				text: needle,
				fontSize: 20,
				fontFamily: 'Helvetica',
				fill: 'black'
			});

			this.layer.add(hr);
			this.layer.add(labelTop);
			this.layer.add(labelBottom);
		}
				
		// add the layer to the stage
		this.stage.add(this.layer);
	}
});

var FancyStitch = StitchPattern.extend({
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


/*
 * Initialization code
 */
$(document).ready(function() {
	var stitch = new StitchPattern;
});