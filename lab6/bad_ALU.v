`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company:  ETH Zurich
// Engineer: Frank K. Gurkaynak
// 
// Create Date:    
// Design Name:    MIPS processor
// Module Name:    bad_ALU 
// Project Name:   Digital Circuits Lab Exercuse
// Target Devices: 
// Tool versions: 
// Description:    This is a poor attempt at writing an ALU
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module bad_ALU( 
    input  [31:0] a, b, 
		input [3:0] aluop, 
		output [31:0] result, 
		output zero);
   
   reg [31:0] slt;       
   reg [31:0] logicsel; 
   
   
   reg [31:0] alu_val; //we need to declare this reg      ////////No reg needed maybe?
   reg [31:0] diff;
   wire ss0; wire ss1; wire Ss2; wire ss3;
   
   assign {ss0,ss1,Ss2,ss3} = aluop; // make assigns

   // define the logicfunction 
   always @ ( * )
   begin
  	if (ss1 == 0)
      if (ss0== 0) logicsel <= a &b; else logicsel <= a | b; ////////Blocking assinment
  	else
      begin
	      if (ss0 == 1)
	        logicsel <= ~(a | b);
	      else logicsel <= a^b;
      end
   end                                            ////////BEGIN-END HERE WAS MISSING

   always @ ( aluop , a, b )
    begin
      if (aluop == 4'b1010)
        begin
	       diff <= a-b;  // calculate the difference   ////////Blocking assignment should have been used
	       slt <= 0;     // default value
	       if (diff[31] == 1) slt<=1; // if MSB is 1 slt is 1 
        end
    end		                                       ////////BEGIN-END HERE WAS MISSING

   always @ ( * )
     begin
    	case (aluop)
              4'b0000 : alu_val <= a + b;       ////////Blocking assinment
              4'b0010 : alu_val <= a - b;
              4'b1011 : alu_val <= slt;
              default : alu_val <= logicsel;
    	endcase		 
     end
   
   assign result = alu_val; 
   assign zero = (alu_val == 32'b0) ? 1: 0;
   
endmodule
