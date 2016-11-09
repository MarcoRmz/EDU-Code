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

//function_definition definition
Blockly.Blocks['function_definition'] = {
  init: function() {
    this.appendValueInput("function_def")
        .setCheck(null)
        .appendField("function")
        .appendField(new Blockly.FieldDropdown([["void", "void"], ["int", "int"], ["float", "float"], ["bool", "bool"], ["string", "string"]]), "function_type")
        .appendField(new Blockly.FieldTextInput(""), "function_id");
    this.appendStatementInput("function_body")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("}");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//parameter1 (no closing) definition
Blockly.Blocks['parameter1'] = {
  init: function() {
    this.appendValueInput("parameter1_value")
        .setCheck(null)
        .appendField("(")
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["bool", "bool"], ["string", "string"]]), "var_type")
        .appendField(new Blockly.FieldTextInput(""), "var_name")
        .appendField(",");
    this.setOutput(true, null);
    this.setColour(105);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//parameter2 closing definition
Blockly.Blocks['parameter2'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["bool", "bool"], ["string", "string"]]), "parameter2_types")
        .appendField(new Blockly.FieldTextInput(""), "parameter2_value")
        .appendField("){");
    this.setOutput(true, null);
    this.setColour(100);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
//empty_parameter definition
Blockly.Blocks['empty_parameter'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("( ){");
    this.setOutput(true, null);
    this.setColour(100);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//var_assign definition
Blockly.Blocks['var_assign'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput(""), "var_id")
        .appendField("=")
        .appendField(new Blockly.FieldTextInput(""), "var_value");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(290);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//main definition
Blockly.Blocks['main'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("main {");
    this.appendStatementInput("main_declaration")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("}");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//endline definition
Blockly.Blocks['endline'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
