module COND (clk, rst, Instruction, Input_1, Input_2, Enable, Output);
  parameter UUID = 0;
  parameter NAME = "";
  input wire clk;
  input wire rst;

  input  wire [15:0] Instruction;
  input  wire [15:0] Input_1;
  input  wire [15:0] Input_2;
  input  wire [0:0] Enable;
  output  wire [0:0] Output;

  TC_Splitter16 # (.UUID(64'd129274797608114045 ^ UUID)) Splitter16_0 (.in(wire_26), .out0(wire_4), .out1());
  TC_Splitter8 # (.UUID(64'd1462455766308944097 ^ UUID)) Splitter8_1 (.in(wire_4), .out0(wire_15), .out1(wire_10), .out2(wire_31), .out3(wire_28), .out4(), .out5(), .out6(), .out7());
  TC_Maker16 # (.UUID(64'd2530465127559157045 ^ UUID)) Maker16_2 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd3318448313327833152 ^ UUID)) Maker16_3 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd1341563485140346365 ^ UUID)) Maker16_4 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd3715244167020249352 ^ UUID)) Maker16_5 (.in0(8'd0), .in1(8'd0), .out());
  TC_Not # (.UUID(64'd3642479983096000307 ^ UUID), .BIT_WIDTH(64'd1)) Not_6 (.in(1'd0), .out());
  TC_Switch # (.UUID(64'd1282100416178726327 ^ UUID), .BIT_WIDTH(64'd1)) Output1z_7 (.en(wire_21), .in(wire_3), .out(Output));
  TC_Switch # (.UUID(64'd2556849178606030734 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_8 (.en(wire_14), .in(wire_8), .out(wire_3_7));
  TC_Switch # (.UUID(64'd3312531434504797649 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_9 (.en(wire_22), .in(wire_13), .out(wire_3_5));
  TC_Switch # (.UUID(64'd202556269158489170 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_10 (.en(wire_23), .in(wire_1), .out(wire_3_3));
  TC_Switch # (.UUID(64'd2040074786646497111 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_11 (.en(wire_5), .in(wire_12), .out(wire_3_0));
  TC_Switch # (.UUID(64'd380134202201595991 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_12 (.en(wire_17), .in(wire_18), .out(wire_3_1));
  TC_Switch # (.UUID(64'd4269170673350230572 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_13 (.en(wire_16), .in(wire_27), .out(wire_3_2));
  TC_Switch # (.UUID(64'd4172599238896292312 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_14 (.en(wire_20), .in(wire_11), .out(wire_3_4));
  TC_Switch # (.UUID(64'd3255056327186087023 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_15 (.en(wire_6), .in(wire_30), .out(wire_3_6));
  TC_Switch # (.UUID(64'd587984888183457986 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_16 (.en(wire_7), .in(wire_32), .out(wire_3_8));
  TC_Switch # (.UUID(64'd4180313715795215094 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_17 (.en(wire_19), .in(wire_33), .out(wire_3_10));
  TC_Equal # (.UUID(64'd2661730651578655407 ^ UUID), .BIT_WIDTH(64'd16)) Equal16_18 (.in0(wire_0), .in1(wire_2), .out(wire_8));
  TC_Not # (.UUID(64'd3321674336245664041 ^ UUID), .BIT_WIDTH(64'd1)) Not_19 (.in(wire_8), .out(wire_13));
  TC_LessU # (.UUID(64'd186987030356888026 ^ UUID), .BIT_WIDTH(64'd16)) LessU16_20 (.in0(wire_0), .in1(wire_2), .out(wire_12));
  TC_LessU # (.UUID(64'd3090816252619095363 ^ UUID), .BIT_WIDTH(64'd16)) LessU16_21 (.in0(wire_0), .in1(wire_2), .out(wire_25));
  TC_LessI # (.UUID(64'd2799939552803634294 ^ UUID), .BIT_WIDTH(64'd16)) LessI16_22 (.in0(wire_0), .in1(wire_2), .out(wire_1));
  TC_LessI # (.UUID(64'd4038549906645841413 ^ UUID), .BIT_WIDTH(64'd16)) LessI16_23 (.in0(wire_0), .in1(wire_2), .out(wire_24));
  TC_Or # (.UUID(64'd3179420809995088507 ^ UUID), .BIT_WIDTH(64'd1)) Or_24 (.in0(wire_8), .in1(wire_24), .out(wire_18));
  TC_Or # (.UUID(64'd3907661087499200637 ^ UUID), .BIT_WIDTH(64'd1)) Or_25 (.in0(wire_8), .in1(wire_25), .out(wire_27));
  TC_Not # (.UUID(64'd1376716593256461201 ^ UUID), .BIT_WIDTH(64'd1)) Not_26 (.in(wire_18), .out(wire_11));
  TC_Not # (.UUID(64'd1218938638150220115 ^ UUID), .BIT_WIDTH(64'd1)) Not_27 (.in(wire_27), .out(wire_30));
  TC_Not # (.UUID(64'd804832623701083752 ^ UUID), .BIT_WIDTH(64'd1)) Not_28 (.in(wire_1), .out(wire_32));
  TC_Not # (.UUID(64'd1902830153822468718 ^ UUID), .BIT_WIDTH(64'd1)) Not_29 (.in(wire_12), .out(wire_33));
  TC_Maker16 # (.UUID(64'd4157917437721305216 ^ UUID)) Maker16_30 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd73664467169810819 ^ UUID)) Maker16_31 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd2242995931664275824 ^ UUID)) Maker16_32 (.in0(8'd0), .in1(8'd0), .out());
  DEC4 # (.UUID(64'd1718291227987089359 ^ UUID)) DEC4_33 (.clk(clk), .rst(rst), .Bit_1(wire_15), .Bit_2(wire_10), .Bit_3(wire_31), .Bit_4(wire_28), .Disable(1'd0), .Output_1(wire_17), .Output_2(wire_16), .Output_3(wire_20), .Output_4(wire_5), .Output_5(wire_23), .Output_6(wire_22), .Output_7(wire_14), .Output_8(wire_9), .Output_9(wire_6), .Output_10(wire_7), .Output_11(wire_19), .Output_12(), .Output_13(), .Output_14(), .Output_15(), .Output_16());
  TC_Switch # (.UUID(64'd2466554002382872020 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_34 (.en(wire_9), .in(wire_29), .out(wire_3_9));
  TC_Constant # (.UUID(64'd2589435540344655957 ^ UUID), .BIT_WIDTH(64'd1), .value(1'd1)) On_35 (.out(wire_29));

  wire [15:0] wire_0;
  assign wire_0 = Input_1;
  wire [0:0] wire_1;
  wire [15:0] wire_2;
  assign wire_2 = Input_2;
  wire [0:0] wire_3;
  wire [0:0] wire_3_0;
  wire [0:0] wire_3_1;
  wire [0:0] wire_3_2;
  wire [0:0] wire_3_3;
  wire [0:0] wire_3_4;
  wire [0:0] wire_3_5;
  wire [0:0] wire_3_6;
  wire [0:0] wire_3_7;
  wire [0:0] wire_3_8;
  wire [0:0] wire_3_9;
  wire [0:0] wire_3_10;
  assign wire_3 = wire_3_0|wire_3_1|wire_3_2|wire_3_3|wire_3_4|wire_3_5|wire_3_6|wire_3_7|wire_3_8|wire_3_9|wire_3_10;
  wire [7:0] wire_4;
  wire [0:0] wire_5;
  wire [0:0] wire_6;
  wire [0:0] wire_7;
  wire [0:0] wire_8;
  wire [0:0] wire_9;
  wire [0:0] wire_10;
  wire [0:0] wire_11;
  wire [0:0] wire_12;
  wire [0:0] wire_13;
  wire [0:0] wire_14;
  wire [0:0] wire_15;
  wire [0:0] wire_16;
  wire [0:0] wire_17;
  wire [0:0] wire_18;
  wire [0:0] wire_19;
  wire [0:0] wire_20;
  wire [0:0] wire_21;
  assign wire_21 = Enable;
  wire [0:0] wire_22;
  wire [0:0] wire_23;
  wire [0:0] wire_24;
  wire [0:0] wire_25;
  wire [15:0] wire_26;
  assign wire_26 = Instruction;
  wire [0:0] wire_27;
  wire [0:0] wire_28;
  wire [0:0] wire_29;
  wire [0:0] wire_30;
  wire [0:0] wire_31;
  wire [0:0] wire_32;
  wire [0:0] wire_33;

endmodule