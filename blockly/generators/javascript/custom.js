//start token
Blockly.JavaScript['start'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = 'start\n';
  return code;
};

//var declaracion
Blockly.JavaScript['var_declaracion'] = function(block) {
  var dropdown_var_type = block.getFieldValue('var_type');
  var text_var_id = block.getFieldValue('var_id');
  // TODO: Assemble JavaScript into code variable.
  var code = dropdown_var_type + ' ' + text_var_id + '\n';
  return code;
};

//function_definition
Blockly.JavaScript['function_definition'] = function(block) {
  var dropdown_function_type = block.getFieldValue('function_type');
  var text_function_id = block.getFieldValue('function_id');
  var value_function_def = Blockly.JavaScript.valueToCode(block, 'function_def', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_function_body = Blockly.JavaScript.statementToCode(block, 'function_body');
  // TODO: Assemble JavaScript into code variable.
  var code = 'function '+dropdown_function_type+' '+text_function_id+''+value_function_def+' {\n'+statements_function_body+'}\n';
  return code;
};

//parameter1 (no closing)
Blockly.JavaScript['parameter1'] = function(block) {
  var dropdown_var_type = block.getFieldValue('var_type');
  var text_var_name = block.getFieldValue('var_name');
  var value_parameter1_value = Blockly.JavaScript.valueToCode(block, 'parameter1_value', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var value_param1 = value_parameter1_value;
  value_param1=value_param1.replace('(','');
  value_param1=value_param1.replace(')','');
  var code = dropdown_var_type+' '+text_var_name+','+value_param1;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

//parameter2 closing
Blockly.JavaScript['parameter2'] = function(block) {
  var dropdown_parameter2_types = block.getFieldValue('parameter2_types');
  var text_parameter2_value = block.getFieldValue('parameter2_value');
  // TODO: Assemble JavaScript into code variable.
  var code = ' '+dropdown_parameter2_types+' '+text_parameter2_value;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

//empty parameter
Blockly.JavaScript['empty_parameter'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '()';
  //return code;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

//var_assign
Blockly.JavaScript['var_assign'] = function(block) {
  var text_var_id = block.getFieldValue('var_id');
  var text_var_value = block.getFieldValue('var_value');
  // TODO: Assemble JavaScript into code variable.
  var code = text_var_id+' = '+text_var_value+'\n';
  return code;
};

//main
Blockly.JavaScript['main'] = function(block) {
  var statements_main_declaration = Blockly.JavaScript.statementToCode(block, 'main_declaration');
  // TODO: Assemble JavaScript into code variable.
  var main_dec = statements_main_declaration.replace('(','')
  main_dec = main_dec.replace(')','')
  var code = 'main {\n' + main_dec+'\n}\n';
  return code;
};

//endline
Blockly.JavaScript['endline'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '\n';
  return code;
};
