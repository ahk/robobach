Boolean {
	*new { ^this.shouldNotImplement(thisMethod) }
	xor { arg bool; ^(this === bool).not }
	if { ^this.subclassResponsibility(thisMethod) }
	not { ^this.subclassResponsibility(thisMethod) }
	&& { ^this.subclassResponsibility(thisMethod) }
	|| { ^this.subclassResponsibility(thisMethod) }
	and { ^this.subclassResponsibility(thisMethod) }
	or { ^this.subclassResponsibility(thisMethod) }
	nand { ^this.subclassResponsibility(thisMethod) }
	
	booleanValue { ^this }
	
	keywordWarnings { 
		// turn on/off warnings if a keyword argument is not found
		_KeywordError 
	} 
	trace { _Trace } // this is only available in a special debugging version of the app
	
	printOn { arg stream;
		stream.putAll(this.asString);
	}
	storeOn { arg stream;
		stream.putAll(this.asCompileString);
	}
	archiveAsCompileString { ^true }
}

True : Boolean {
	if { arg trueFunc, falseFunc; ^trueFunc.value }
	not { ^false }
	&& { arg that; ^that.value }
	|| { arg that; ^this }
	and { arg that; ^that.value }
	or { arg that; ^this }
	nand { arg that; ^that.value.not }
	binaryValue { ^1 }
}

False : Boolean  {
	if { arg trueFunc, falseFunc; ^falseFunc.value }
	not { ^true }
	&& { arg that; ^this }
	|| { arg that; ^that.value }
	and { arg that; ^this }
	or { arg that; ^that.value }
	nand { arg that; ^true }
	binaryValue { ^0 }
}
