# translator
化学描述自动合成语言

#测试脚本
#-*- coding : utf-8 -*-  
# coding: utf-8  
from synthreader import text_to_xdl  
from xdl.utils.graph import get_graph  
import networkx as nx   
import matplotlib  
import matplotlib.pyplot as plt  
  
#s = 'Acetic acid (125 mL) was added with stirring and the mixture heated at 87 °C for 15 hours.'  
#第一步  
s = 'A MeNH2 aqueous solution (40%, 19.9 mL, 230.5 mmol) was added dropwise to ethyl acetoacetate (9.7 mL, 76.8 mmol) in jacketed filter while stirring. The reaction was stirred at 0 °C for 3 h, and then diluted with CH2Cl2 (100 mL) and H2O (50 mL). The organic layer was separated, dried over anhydrous MgSO4, and concentrated at 30 °C to afford the enamine Yield: 658 mg, 92%; yellow oil.'  
#第二步  
s = 'In a 250 mL round bottom flask Benzoquinone (12.40 g, 0.11 mol) was dissolved in acetone (120 mL). The mixture was heated to 30 °C, a solution of ethyl-3-methyl amino crotonate (17.199 mL, 0.11 mol) was added dropwise upon stirring at this temperature for 2 h. After cooling to room temperature, the reaction mixture was concentrated in vacuo and the residue was purified by recrystallization with acetone to afford the product as solid.'  
#第三步  
s = '3 g of indole derivative was dissolved in 3.1 mL pyridine (3.0 eq.) and to the above solution was added 24.3 mL acetic anhydride (20 eq.). The reaction was stirred and heated to 150 °C. After 1 h, the reaction was allowed to cool back to rt before being diluted with ethyl acetate (40 mL). The mixture was washed with a solution of aqueous saturated sodium bicarbonate (40 mL). The product was extracted with ethyl acetate (2 x 40 mL) and the combined organic layers were washed with water (40 mL), dried over anhydrous MgSO4 and concentrated under vacuum to afford the product as a white solid which was used without further purification.'  
#第四步  
s = '1.0 g of indole derivative was dissolved in carbon tetrachloride (100 mL) and Bromine (0.558 mL) was added to the above-stirred solution. After heating at 85 °C for 16 h, the reaction was cooled and 100 mL of sodium thiosulphate solution (10% w/v in water) was added and the mixture was stirred for 20 min at room temperature until the orange color disappeared. After this time, the reaction mixture was transferred into a separation funnel, the reactor was rinsed with 10 mL of carbon tetrachloride and the organic phase was separated and washed with water (2 x 100 mL), dried (MgSO4). The mixture was concentrated under vacuum at 40 °C and 40 mbar to afford a pale yellow solid, which was used without further purification (1.40 g).'  
#第五步  
s = 'Potassium hydroxide (763 mg, 3.0 equiv.) was dissolved in methanol (16 mL) and to the above solution was added 0.7 mL of thiophenol (1 equiv.) and the mixture was stirred at room temperature for 15 min. After this time, the solution was cooled to 0 °C and 3.0 g of Bromo indole derivative in 24 mL dichloromethane was added. The reaction was stirred for 3 h before neutralization with 1.2 mL of acetic acid. The solvent was removed in vacuum and the product was purified on silica gel using 20% EtOAc in hexane to yield the title product as a pale yellow solid.'  
#第六步  
s = '9.55 g of indole derivative was dissolved in 59 ml of dioxane and to the above solution was added 6.25 ml of bis(dimethylamino)methane. The mixture was heated to 105 °C for 3 h, cooled, and diluted with 300 mL of water. The crystals that formed were separated, washed with water, and dried. Yield: 60.1 g (70%) of V, mp 125-126.'   
#第七步  
s = '47.1 g (0.098 mole) of Arbidol was dissolved in 280 mL of acetone while stirring and heated to 60 °C.  To the above solution was added 11 mL of concentrated hydrochloric acid. The reaction mixture was cooled to 10 °C and the precipitate was filtered off and recrystallized from an acetone-methanol-hydrochloric acid (700:85:7.5) mixture. Yield: 45.1 g (86%) of hydrochloric acid of Arbidol.'  
  
xdl = text_to_xdl(s)   
print(xdl)  
G = get_graph("D://HSZD//ChemputerAntiviralXDL-master//Arbidol//XDL//Step1//graph.json")  
nx.draw(G,  
        pos = nx.random_layout(G), # pos 指的是布局,主要有spring_layout,random_layout,circle_layout,shell_layout  
        node_color = 'b',   # node_color指节点颜色,有rbykw,同理edge_color   
        edge_color = 'r',  
        with_labels = True,  # with_labels指节点是否显示名字   
        font_size =18,  # font_size表示字体大小,font_color表示字的颜色  
        node_size =20)  # font_size表示字体大小,font_color表示字的颜色  
#plt.savefig("network.png")  
plt.show()  
