Includes = {
}

PixelShader =
{
	Samplers =
	{
		TextureOne =
		{
			Index = 0
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		TextureTwo =
		{
			Index = 1
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
	}
}


VertexStruct VS_INPUT
{
    float4 vPosition  : POSITION;
    float2 vTexCoord  : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
    float4  vPosition : PDX_POSITION;
    float2  vTexCoord0 : TEXCOORD0;
};


ConstantBuffer( 0, 0 )
{
	float4x4 WorldViewProjectionMatrix; 
	float4 vFirstColor;
	float4 vSecondColor;
	float CurrentState;
};


VertexShader =
{
	MainCode VertexShader
	[[
		
		VS_OUTPUT main(const VS_INPUT v )
		{
			VS_OUTPUT Out;
		   	Out.vPosition  = mul( WorldViewProjectionMatrix, v.vPosition );
			Out.vTexCoord0  = v.vTexCoord;
			Out.vTexCoord0.y = -Out.vTexCoord0.y;
		
			return Out;
		}
		
	]]
}

PixelShader =
{
	MainCode PixelColor
	[[
		
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			return vFirstColor;
		}
		
	]]

	MainCode PixelTexture
	[[
		
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float4 OutColor = tex2D( TextureOne, v.vTexCoord0 );
			
			int CurrentStateInt = (int)(CurrentState * 100);
			float3 partyRGBValue;
			
			switch(CurrentStateInt)
			{
				case 0:		//LEFT
					partyRGBValue = float3(0.517647f, 0.090196f, 0.396078f);
					//RGB: 132, 23, 101
					break;
					
				case 1: 	//PO
					partyRGBValue = float3(1.0f, 0.4f, 0.0f);
					//RGB: 255, 102, 0
					break;
					
				case 2: 	//PSL
					partyRGBValue = float3(0.243137f, 0.7058823f, 0.239215f);
					//RGB: 62, 180, 61
					break;
					
				case 3: 	//PiS
					partyRGBValue = float3(0.0039215f, 0.168627f, 0.50588235f);
					//RGB: 1, 43, 129
					break;
					
				case 4: 	//RIGHT
					partyRGBValue = float3(0.0509803f, 0.145098f, 0.270588236f);
					//RGB: 13, 37, 69
					break;
					
				default:	//Default / other
					partyRGBValue = float3(0.5490196f, 0.5490196f, 0.5490196f);
					//RGB: 140, 140, 140
					break;
			}
			
			//Perform colour burn operation with OutColor.rgb over the party colour
			float3 colourBurnOut = 1 - partyRGBValue;
			colourBurnOut = 1 - (colourBurnOut / OutColor.rgb);
			OutColor.rgb = colourBurnOut;


			return OutColor;
		}
		
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
}


Effect Color
{
	VertexShader = "VertexShader"
	PixelShader = "PixelColor"
}

Effect Texture
{
	VertexShader = "VertexShader"
	PixelShader = "PixelTexture"
}

