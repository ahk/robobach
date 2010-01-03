// idea by adc, mods by /f0, jrh, mc, ...
	var <prevKrNames, <prevArNames;
	var <scrollyAr, <keysRotationAr=0; 
	var <scrollyKr, <keysRotationKr=0; 
	
	*initClass { 
		GUI.skins.put(\jit, (
				fontSpecs: 	["Helvetica", 10],
				fontColor: 	Color.black,
				background: 	Color(0.8, 0.85, 0.7, 0.5),
				foreground:	Color.grey(0.95),
				onColor:		Color(0.5, 1, 0.5), 
				offColor:		Color.clear,
				gap:			0 @ 0,
				margin: 		2@2,
				buttonHeight:	16
			)
		);
	}
	
		font = GUI.font.new(*skin.fontSpecs);
		
			.background_(skin.foreground);
			.background_(skin.foreground);		
			.background_(skin.foreground);
		
		scrollyAr = EZScroller.new(w, 
			Rect(compArZone.bounds.right - 16, 30, 12, nProxies * skin.buttonHeight), 
			nProxies, nProxies, 
			{ |sc| keysRotationAr = sc.value.asInteger.max(0); }
		).value_(0).visible_(true);

	}
		var emergencySynth;

		GUI.staticText.new(compKrZone, Rect(0, 0, 180, 18))
			.font_(font).align_(\center)
			.string_("kr proxies");
			
		layout.nextLine;
		layout.shift(0,4);
		
		/*
			pausBtn = GUI.button.new(compKrZone, Rect(0,0, 30, skin.buttonHeight))
				.font_(font).states_([["paus", Color.black, skin.onColor], 
				["rsum", Color.black, Color.clear]])
				.action_({ |btn|
					var editName = nameBtn.string.asSymbol;
					var px = proxyspace.envir[editName];
					if (px.notNil) { 
						if (px.paused) { px.resume } { px.pause };
					};
				});
			sendBtn = GUI.button.new(compKrZone, Rect(0,0, 30, skin.buttonHeight))
				.font_(font).states_([["send", Color.black, skin.onColor]])
				.action_({ |btn|
					var editName = nameBtn.string.asSymbol;
					var px = proxyspace.envir[editName];
					if (px.notNil) { px.send };
				});
			
			pollBtn = GUI.button.new(compKrZone, Rect(0,0, 24, skin.buttonHeight))
				.font_(font).states_([["poll", Color.black, skin.foreground]])
				.action_({ 
					var editName = nameBtn.string.asSymbol;
					var px = proxyspace.envir[editName];
					if (px.notNil) { 
						px.bus.getn(px.numChannels, { |arr| [editName, arr.unbubble].postln });
					};
				});
			editBtn = GUI.button.new(compKrZone, Rect(0,0,20, skin.buttonHeight)).states_([
				["ed", skin.fontcolor, Color.new(0.7,0.7,0.7,1)],
				["ed", skin.fontcolor, Color.white]])
				.action_({ arg btn;	
					var editName = nameBtn.string.asSymbol;
					editor.proxy_(proxyspace.envir[editName]);
					this.update;
					this.openEditZone(1);
					editBtnsAr.do { |b| b.value_(0) };
					editBtnsKr.do { |b| b.value_(0) };
					btn.value_(1);
				}).font_(font);

			
		editBtnsKr = buttonLinesKr.collect(_[1]);

		scrollyKr = EZScroller.new(w, 
			Rect(compKrZone.bounds.right - 16, 30, 12, nProxies * skin.buttonHeight), 
			nProxies, nProxies, 
			{ |sc| keysRotationKr = sc.value.asInteger.max(0); }
		).value_(0).visible_(true);

	}

		if (krProxyNames.size > nProxies) { 

			scrollyKr.visible_(true)
				.numItems_(krProxyNames.size)
				.value_(keysRotationKr ? (krProxyNames.size - nProxies)); 
				
			krProxyNames = krProxyNames.drop(keysRotationKr).keep(nProxies);
		} {
			scrollyKr.visible_(false);
		}; 

		if (krProxyNames != prevKrNames) { 
				
				butLine = buttonLinesKr[i];
				nameSink = butLine[0];
				
		};
		prevKrNames = krProxyNames;
			scrollyAr.visible_(true)
				.numItems_(arPxNames.size)
				.value_(keysRotationAr ? (arPxNames.size - nProxies)); 
				
			scrollyAr.visible_(false);
		}; 
		
		}; 
		arPxNames.do { |name, i| pxMons[i].updateAll };
		
		prevArNames = arPxNames;


NdefMixer : ProxyMixer { 
	
	*new { |server, nProxies = 16, title, bounds|	
		var space; 
		if (server.isKindOf(Symbol)) { 
			server = Server.named.at(server);
			if (server.isNil) { Error("NdefMixer: no server named %.".format(server)).throw };
		} { 
			server = server ? Ndef.defaultServer ? Server.default; 
		};
		
		space = Ndef.dictFor(server);
		
		title = title ? ("Ndef:" + server.name);
		^super.new(space, nProxies, title, bounds);
	}
}