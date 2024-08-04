Includes = {
	"buttonstate.fxh"
}

PixelShader =
{
	Samplers =
	{
		MapTexture =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
	}
}


VertexStruct VS_OUTPUT
{
	float4  vPosition : PDX_POSITION;
	float2  vTexCoord : TEXCOORD0;
};


VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
		    VS_OUTPUT Out;
		    Out.vPosition  = mul( WorldViewProjectionMatrix, float4( v.vPosition.xyz, 1 ) );
		
		    Out.vTexCoord = v.vTexCoord;
			Out.vTexCoord += Offset;
		
		    return Out;
		}
	]]
}

PixelShader =
{
	MainCode PixelShaderTriangleFade
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
		    float4 OutColor = tex2D( MapTexture, v.vTexCoord );
			
			//Partitions to code into two parts: One part before 'triangleVertex', and one part after.
			//triangleVertex is a float between 0 and 1 that measures how far along the X-axis the image is.
			//The image on the left is treated as almost it's own image. localX is a float between 0 and 1
			//that  defines the distance of the point between triangleVertex and the end of the image.
			
			//We then just see if the sum of localX and v.vTexCoord.y is greater than one, dividing the second part of the image in to diagonally
			
			
			float triangleVertex = 1 - (100.0f / 360.0f);
			
			OutColor.a = 1- v.vTexCoord.x;
			if ( v.vTexCoord.x > triangleVertex){
				float localX = (v.vTexCoord.x - triangleVertex) * 3.60;		//Equal to 360/100, change depending on your previous variable
				
				if ((localX + v.vTexCoord.y) > 1){
					OutColor.a = 0;
				}
				//else{		//Code can be put here to effect the top triangle
				//	OutColor.a = 1;
				//}
			}

			return OutColor;
		}	
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
}


Effect Up
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderTriangleFade"
}

Effect Down
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderTriangleFade"
}

Effect Disable
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderTriangleFade"
}

Effect Over
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderTriangleFade"
}

