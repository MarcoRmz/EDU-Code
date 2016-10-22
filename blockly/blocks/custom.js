'use strict';

goog.provide('Blockly.Blocks.custom');

goog.require('Blockly.Blocks');

//start block definition
Blockly.Blocks['start'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Start");
    this.setNextStatement(true, null);
    this.setColour(255);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
