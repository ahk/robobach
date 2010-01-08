
	var <skin, <font;

	var <>w, <zone, <nameView, <typeChanView, <monitor,
		<>nSliders, <edits, <sinks, <scrolly, skipjack;
	var buttonFuncs, pauseBut, sendBut;
	
	var 	<currentSettings, 	<prevSettings, <editKeys, <>ignoreKeys=#[];
	var 	<tooManyKeys = false, <keysRotation = 0; 	

	*initClass { 
		StartUp.add{
			Spec.add(\ampx4, [0, 4, \amp]);
			Spec.add(\fadePx, [0, 100, \amp, 0, 0.02]); 
		};
	}
	
		monitor=true, sinks=true, morph=false; 
		
			.init(win, comp, extras, monitor, sinks, morph)
		var typeStr;
		if (px.isNil) { 
			proxy = nil; 
			nameView.object_(px).string_('-');
			typeChanView.string_('-'); 
			this.fullUpdate;
		} { 
						if(proxy.rate === 'control', { "kr" }, { "ir" })
						} +  proxy.numChannels;
				typeChanView.string_(typeStr);
				if (monitor.notNil) { monitor.proxy_(proxy) };
		}
	
	name { ^nameView.string.asSymbol }
	name_ { |key| nameView.string_(key.asString); }
	
		// backwards compatibility
	pxKey { ^this.name }
	pxKey_ { |key| ^this.name_(key) }

		
				
			// "NodeProxyEditor: making internal win.".postln; 
			Window(this.class.name, bounds.resizeBy(4, 4)) 
		};
			// "NodeProxyEditor: making internal zone.".postln;  
			CompositeView(w, bounds); 
		};
		replaceKeys = replaceKeys ?? { () };
		
		this.makeButtonFuncs; 
		
		
	
			zone.bounds.width - 4 @ (skin.buttonHeight), 
			showName: false, makeWatcher: false);
		inform("NodeProxyEditor: preset/morph not finished yet.");

		nameView.setBoth_(false)
			.receiveDragHandler = { this.proxy_(View.implClass.currentDrag) };
			
		typeChanView = StaticText(zone, 30@menuHeight).string_("ar 88").align_(0).font_(font);
		
		extras.do { |butkey| 
			buttonFuncs[butkey].value;	
		};
		
		zone.decorator.nextLine.shift(0, 4);
	
		
			ez.visible_(false);
			
			ez.sliderView.keyDownAction = { |view, char,modifiers,unicode,keycode| 
				if (unicode == 127) { // delete key
					try { proxy.unset(ez.labelView.string.asSymbol) }
				} { 
					view.defaultKeyDownAction(char,modifiers,unicode,keycode);
				};
			};
			[ez, sink]

		lay = zone.decorator; 
		lay.left_(lay.bounds.right - 20).top_(lay.bounds.top + 48);
		
		scrolly = EZScroller(zone, 
			Rect(0, 0, 14, nSliders * skin.buttonHeight), 
			nSliders, nSliders, 
			{ |sc| keysRotation = sc.value.asInteger; }
		).visible_(false);
		[\scrolly, scrolly.slider.bounds];
	}

	makeButtonFuncs { 
		buttonFuncs = (
			CLR: { Button(zone, 30@20).font_(font)
					.states_([[\CLR, skin.fontColor, Color.clear]])
					.action_({ arg btn, mod; 
						if ([524576, 24].includes(mod) ) { 
							proxy.clear 
						} { 
							"use alt-click to clear proxy.".postln;
						} 
					}) 
			},
				
			reset: { Button(zone, 30@20).font_(font)
					.states_([[\reset, skin.fontColor, Color.clear]])
					.action_({ proxy !? { proxy.nodeMap = ProxyNodeMap.new; this.fullUpdate; } }) 
			},

			pausR: { pauseBut = Button(zone, 30@20).font_(font)
					.states_([
							["paus", skin.fontColor, skin.onColor], 
							["rsum", skin.fontColor, skin.offColor]
						])
					.action_({ arg btn; proxy !? {
								[ { proxy.resume; }, { proxy.pause; }  ].at(btn.value).value;
							} });
				},

			sendR: 	{ sendBut = Button(zone, 30@20).font_(font)
						.states_([ 
							["send", skin.fontColor, skin.offColor], 
							["send", skin.fontColor, skin.onColor] 
						])
						.action_({ arg btn, mod; 
									//	mod.postln;
							if(proxy.notNil and: (btn.value == 0)) { 
								// alt-click osx, swingosc
								if ([524576, 24].includes(mod) ) { proxy.rebuild } { proxy.send }
							};
							btn.value_(1 - btn.value)
						})
			},

			scope: 	{ Button(zone, 36@20).font_(font)
						.states_([[\scope, skin.fontColor, Color.clear]])
						.action_({ proxy !? { proxy.scope } }) 
			},
			
			doc: 	{ Button(zone, 30@20).font_(font)
						.states_([[\doc, skin.fontColor, Color.clear]])
						.action_({ |but, mod|
							if ([524576, 24].includes(mod) ) { 
								NodeProxyEditor(proxy) 
							} {  
							if(proxy.notNil and: currentEnvironment.isKindOf(ProxySpace)) { 
								currentEnvironment.document(proxy.key)
									.title_("<" + proxy.key.asString + ">") 
							} {
								"can't currently document a proxy outside a proxy space.".inform;
							} }
						}) 
			}, 

			end: 	{ Button(zone, 24@20).font_(font)
					.states_([[\end, skin.fontColor, Color.clear]])
					.action_({ proxy !? {  proxy.end } }) 
			},
			
			fade: 	{ var nb = EZNumber(zone, 60@20, \fade, \fadePx, 
								{ |num| proxy.fadeTime_(num.value) }, 
								try { proxy.fadeTime } ? 0.02, 
								labelWidth: 24, 
								numberWidth: 32);
						nb.labelView.font_(font).background_(Color.clear);
						nb.numberView.font_(font).background_(Color.clear);
			},
				
				// extras:

			rip: 	{ Button(zone, 15@20).font_(font)
						.states_([['^', skin.fontColor, Color.clear]])
						.action_({ this.class.new(proxy, nSliders) }) 
			},


			wake: 	{ Button(zone, 30@20).font_(font)
						.states_([[\wake, skin.fontColor, Color.clear]])
						.action_({  proxy !? { proxy.wakeUp } }) 
			},
				
			send: 	{ Button(zone, 30@20).font_(font)
						.states_([[\send, skin.fontColor, Color.clear]])
						.action_({  proxy !? { proxy.send } }) 
			},
				
			rebuild: 	{ Button(zone, 30@20).font_(font)
						.states_([[\rbld, skin.fontColor, Color.clear]])
						.action_({  proxy !? { proxy.rebuild } }) 
			}
				
//			poll: 	{ Button(zone, 30@20).font_(font)
//				.states_([[\poll, skin.fontColor, Color.clear]])
//				.action_({  proxy !? { proxy.poll } }) },
//
//						// show a little amp view?
//			amp: 	{ Button(zone, 30@20).font_(font)
//				.states_([[\amp, skin.fontColor, Color.clear]])
//				.action_({ "// show a little amp view?".postln }) }
				
		);
	}
	
	checkTooMany { 
		var oversize = (editKeys.size - nSliders).max(0);
		tooManyKeys = oversize > 0;
		keysRotation = keysRotation.clip(0, oversize);
		
		if (tooManyKeys) { 
		//	"tooManyKeys...".postln;

			scrolly.visible_(true);
			scrolly.numItems_(editKeys.size);
			editKeys = editKeys.drop(keysRotation).keep(nSliders);
			currentSettings = currentSettings.drop(keysRotation).keep(nSliders);
		} {	
		//	"plenty of space.".postln;
			scrolly.numItems_(editKeys.size);
			scrolly.visible_(false);
		};
		scrolly.value_( keysRotation);
	}
	
		
		this.checkTooMany;
		
		// [\oldKeys, oldKeys, \editKeys, editKeys].printAll;
		
		if (monitor.notNil) { monitor.updateAll }; 

			if (pauseBut.notNil) { 
				pauseBut.value_((proxy.notNil and: { proxy.paused }).binaryValue) 
			};
			if (sendBut.notNil) { 
				sendBut.value_((proxy.notNil and: { proxy.objects.notEmpty }).binaryValue) 
			};
		
		this.checkTooMany;
		
	//	"updateVals : ".postln;
		if (currentSettings == prevSettings) {
		 //	"no change.".postln;
			^this;
		};
		
	//	"values have changed - updating edits.".postln; 
		
		editKeys.do { arg key, i;
			if (val != try { prevSettings[i][1] }) { 
					// disable for arrayed controls
				sl.enabled_(val.size <= 1);		 
			};
		prevSettings = currentSettings; 
		var replaced;
		if (replaceKeys.isNil) { ^key };
		replaced = replaceKeys[key.asSymbol];
		if (replaced.isNil) { ^key };
	//	"NPXE: replacing % with %.".format(key.asCompileString, replaced.asCompileString).postln;
		^replaced;
		 
	}
	//	var keyPressed = false;
		if (proxy.isNil) { 
			[sinks, edits].do(_.do(_.visible_(false)));
			^this;
		};
		
		edits.do { arg sl, i;
			var key, val, mappx, spec, slider, number, sink, mapKey;
			var keyString, labelKey, isWet, isMix; 
			
			key = editKeys[i];
			sink = sinks[i];
			
			if(key.notNil) { 
				// editKeys and currentSettings are in sync.
				val = currentSettings[i][1];	
				
				labelKey = key;
				keyString = key.asString;
				spec = key.asSpec;

				isWet = keyString.beginsWith("wet"); // a filtered slot
				isMix = keyString.beginsWith("mix");	// an additive source
					
				if (isWet or: isMix) { 
					if (isWet) { spec = \amp.asSpec };
					if (isMix) { spec = \amp4.asSpec };
					sl.sliderView.background_(Color.green(1.0, 0.5)).refresh;
					sl.labelView.background_(Color.green(1.0, 0.5)).refresh;
				} { 
					sl.sliderView.background_(skin.foreground).refresh;
					sl.labelView.background_(skin.foreground).refresh;
				};
				sl.visible_(true);
				
				sl.labelView.string = this.replaceName(key);
				sl.sliderView.enabled = spec.notNil;
				sl.sliderView.visible = spec.notNil;
				sl.numberView.enabled = true;
				sl.numberView.visible = true;
				sl.labelView.visible = true;
				sink.visible = true;						
	//			sl.sliderView.keyDownAction = { keyPressed = true }; // doesn't work yet.
	//			sl.sliderView.keyUpAction = {  proxy.xset(key, sl.value); keyPressed = false };

				sl.action_({ arg nu; proxy.set(key, nu.value) });
				
				if(spec.notNil) { sl.controlSpec = spec } {
					sl.controlSpec = ControlSpec(-1e8, 1e8);
				};
				
				mappx = val.value ? 0; 
				if(mappx.isNumber) {
					sl.value_(mappx ? 0);
					sink.object_(nil).string_("-");
				} {	
						// assume mappx is a proxy:
					if (val.isKindOf(BusPlug), { 
						mapKey = currentEnvironment.findKeyForValue(mappx) ? "???";
						sink.object_(mapKey).string_(mapKey);
						sl.labelView.string = "->" + key;
					});				
				}
			}  {		
				// "// hide unused edits".postln;
				sink.object_(nil).string_("-").visible_(false);
				sl.labelView.background_(skin.foreground).string_("");
				sl.sliderView.background_(skin.foreground);
				sl.visible_(false);
			};
		};
		// this.adjustWindowSize;
	}