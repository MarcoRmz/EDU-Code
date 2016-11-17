'use strict';

goog.provide('Blockly.Blocks.custom');

goog.require('Blockly.Blocks');

//start block definition
Blockly.Blocks['start'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("start");
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

//if statement definition
Blockly.Blocks['if_statement'] = {
  init: function() {
    this.appendValueInput("if")
        .setCheck(null)
        .appendField("if");
    this.appendStatementInput("if_block")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("}");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(195);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
//else if
Blockly.Blocks['elseif_statement'] = {
  init: function() {
    this.appendValueInput("elseif")
        .setCheck(null)
        .appendField("elseif ");
    this.appendStatementInput("bloque")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("}");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(195);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
//condicion
Blockly.Blocks['condicion'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("(")
        .appendField(new Blockly.FieldTextInput(""), "condicion")
        .appendField("){");
    this.setOutput(true, null);
    this.setColour(195);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
//dowhile definition
Blockly.Blocks['do_while'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("do {");
    this.appendStatementInput("do_while_bloque")
        .setCheck(null);
    this.appendValueInput("d_while")
        .setCheck(null)
        .appendField("}while");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(0);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
//from to by definition
Blockly.Blocks['from_to_by'] = {
  init: function() {
    this.appendValueInput("from")
        .setCheck(null)
        .appendField("from")
        .appendField(new Blockly.FieldTextInput(""), "from_num")
        .appendField("to")
        .appendField(new Blockly.FieldTextInput(""), "to_num")
        .appendField("by");
    this.appendStatementInput("from_bloque")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("}");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(0);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//by + definition
Blockly.Blocks['by_plus'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("(+")
        .appendField(new Blockly.FieldTextInput(""), "bp_num")
        .appendField("){");
    this.setOutput(true, null);
    this.setColour(0);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
//by - definition
Blockly.Blocks['by_minus'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("( -")
        .appendField(new Blockly.FieldTextInput(""), "bm_num")
        .appendField("){");
    this.setOutput(true, null);
    this.setColour(0);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//by * definition
Blockly.Blocks['by_mult'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("( *")
        .appendField(new Blockly.FieldTextInput(""), "bmult_num")
        .appendField("){");
    this.setOutput(true, null);
    this.setColour(0);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
//by / definition
Blockly.Blocks['by_div'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("( / ")
        .appendField(new Blockly.FieldTextInput(""), "bd_num")
        .appendField("){");
    this.setOutput(true, null);
    this.setColour(0);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
//while definition
Blockly.Blocks['while'] = {
  init: function() {
    this.appendValueInput("while")
        .setCheck(null)
        .appendField("while");
    this.appendStatementInput("while_bloque")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("}");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(0);
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
//end definition
Blockly.Blocks['end'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("end");
    this.setPreviousStatement(true, null);
    this.setColour(255);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
