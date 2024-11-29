module DEC2 (clk, rst, Input_1, Input_2, Disable, Output_1, Output_2, Output_3, Output_4);
  parameter UUID = 0;
  parameter NAME = "";
  input wire clk;
  input wire rst;

  input  wire [0:0] Input_1;
  input  wire [0:0] Input_2;
  input  wire [0:0] Disable;
  output  wire [0:0] Output_1;
  output  wire [0:0] Output_2;
  output  wire [0:0] Output_3;
  output  wire [0:0] Output_4;

  TC_Decoder2 # (.UUID(64'd4359427973961977160 ^ UUID)) Decoder2_0 (.sel0(wire_7), .sel1(wire_8), .out0(wire_3), .out1(wire_5), .out2(wire_0), .out3(wire_6));
  TC_Switch # (.UUID(64'd941765201135534263 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_1 (.en(wire_1), .in(wire_3), .out(wire_2));
  TC_Switch # (.UUID(64'd4032606018154704839 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_2 (.en(wire_1), .in(wire_5), .out(wire_4));
  TC_Switch # (.UUID(64'd4190596213735069994 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_3 (.en(wire_1), .in(wire_0), .out(wire_10));
  TC_Switch # (.UUID(64'd1979495537162252549 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_4 (.en(wire_1), .in(wire_6), .out(wire_9));
  TC_Not # (.UUID(64'd2437088790841561029 ^ UUID), .BIT_WIDTH(64'd1)) Not_5 (.in(wire_11), .out(wire_1));

  wire [0:0] wire_0;
  wire [0:0] wire_1;
  wire [0:0] wire_2;
  assign Output_4 = wire_2;
  wire [0:0] wire_3;
  wire [0:0] wire_4;
  assign Output_1 = wire_4;
  wire [0:0] wire_5;
  wire [0:0] wire_6;
  wire [0:0] wire_7;
  assign wire_7 = Input_1;
  wire [0:0] wire_8;
  assign wire_8 = Input_2;
  wire [0:0] wire_9;
  assign Output_3 = wire_9;
  wire [0:0] wire_10;
  assign Output_2 = wire_10;
  wire [0:0] wire_11;
  assign wire_11 = Disable;

endmodule
