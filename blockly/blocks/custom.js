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

//var declaracion definition
Blockly.Blocks['var_declaracion'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["string", "string"], ["bool", "bool"]]), "var_type")
        .appendField(new Blockly.FieldTextInput(""), "var_id");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
