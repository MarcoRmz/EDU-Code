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
  var code = ' ';
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
  var code = 'main {\n' + statements_main_declaration+'\n}\n';
  return code;
};

//if statement
Blockly.JavaScript['if_statement'] = function(block) {
  var value_if = Blockly.JavaScript.valueToCode(block, 'if', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_if_block = Blockly.JavaScript.statementToCode(block, 'if_block');
  // TODO: Assemble JavaScript into code variable.
  var code = 'if '+value_if+' {\n'+statements_if_block+'\n}\n';
  return code;
};
//elseif statement
Blockly.JavaScript['elseif_statement'] = function(block) {
  var value_elseif = Blockly.JavaScript.valueToCode(block, 'elseif', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_bloque = Blockly.JavaScript.statementToCode(block, 'bloque');
  // TODO: Assemble JavaScript into code variable.
  var code = 'elseif '+value_elseif+'{\n'+statements_bloque+'\n}\n';

  return code;
};

//condicion
Blockly.JavaScript['condicion'] = function(block) {
  var text_condicion = block.getFieldValue('condicion');
  // TODO: Assemble JavaScript into code variable.
  var code = text_condicion;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};
//do while
Blockly.JavaScript['do_while'] = function(block) {
  var statements_do_while_bloque = Blockly.JavaScript.statementToCode(block, 'do_while_bloque');
  var value_d_while = Blockly.JavaScript.valueToCode(block, 'd_while', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = 'do {\n'+statements_do_while_bloque+'\n}while '+value_d_while+"\n";
  return code;
};
//from to by
Blockly.JavaScript['from_to_by'] = function(block) {
  var text_from_num = block.getFieldValue('from_num');
  var text_to_num = block.getFieldValue('to_num');
  var value_from = Blockly.JavaScript.valueToCode(block, 'from', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_from_bloque = Blockly.JavaScript.statementToCode(block, 'from_bloque');
  // TODO: Assemble JavaScript into code variable.
  var code = 'from '+text_from_num+" to "+text_to_num + " by "+value_from + '{\n'+statements_from_bloque+'}\n';
  return code;
};

//by plus
Blockly.JavaScript['by_plus'] = function(block) {
  var text_bp_num = block.getFieldValue('bp_num');
  // TODO: Assemble JavaScript into code variable.
  var code = "+ "+text_bp_num;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

//by minus
Blockly.JavaScript['by_minus'] = function(block) {
  var text_bm_num = block.getFieldValue('bm_num');
  // TODO: Assemble JavaScript into code variable.
  var code = "- " + text_bm_num;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

//by mult
Blockly.JavaScript['by_mult'] = function(block) {
  var text_bmult_num = block.getFieldValue('bmult_num');
  // TODO: Assemble JavaScript into code variable.
  var code = "* "+text_bmult_num;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

//by div
Blockly.JavaScript['by_div'] = function(block) {
  var text_bd_num = block.getFieldValue('bd_num');
  // TODO: Assemble JavaScript into code variable.
  var code = "/ "+text_bd_num;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

//while
Blockly.JavaScript['while'] = function(block) {
  var value_while = Blockly.JavaScript.valueToCode(block, 'while', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_while_bloque = Blockly.JavaScript.statementToCode(block, 'while_bloque');
  // TODO: Assemble JavaScript into code variable.
  var code = "while "+value_while+"{\n"+statements_while_bloque+"\n}\n";
  return code;
};

//endline
Blockly.JavaScript['endline'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '\n';
  return code;
};
//end
Blockly.JavaScript['end'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = 'end\n';
  return code;
};
