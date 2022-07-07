using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Macropad_Customisation_GUI_Forms
{
    public partial class Form1 : Form
    {
        List<MacroLayer> macroPad = new List<MacroLayer>();
        int currentLayer = 0;
        int currentButton = 0;
        public IDictionary<int, string> MacroKey = new Dictionary<int, string>();
        public Form1()
        {
            InitializeComponent();
            InitialiseKey();
            MacroLayer ml = new MacroLayer();
            ml.SetUpDefaultButtons(MacroKey);
            macroPad.Add(ml);
            UpdateScreen();
        }
        private void UpdateScreen()
        {
            btnOne.Text = macroPad[currentLayer].GetButtonName(0);
            btnTwo.Text = macroPad[currentLayer].GetButtonName(1);
            btnThree.Text = macroPad[currentLayer].GetButtonName(2);
            btnFour.Text = macroPad[currentLayer].GetButtonName(3);
            btnFive.Text = macroPad[currentLayer].GetButtonName(4);
            btnSix.Text = macroPad[currentLayer].GetButtonName(5);
            btnSeven.Text = macroPad[currentLayer].GetButtonName(6);
            btnEight.Text = macroPad[currentLayer].GetButtonName(7);
            btnNine.Text = macroPad[currentLayer].GetButtonName(8);
            txtVisPadDisplay.Text = macroPad[currentLayer].GetLayerName();
        }
        private void InitialiseKey()
        {
            MacroKey.Add(new KeyValuePair<int, string>(0, "One"));
            MacroKey.Add(new KeyValuePair<int, string>(1, "Two"));
            MacroKey.Add(new KeyValuePair<int, string>(2, "Three"));
            MacroKey.Add(new KeyValuePair<int, string>(3, "Four"));
            MacroKey.Add(new KeyValuePair<int, string>(4, "Five"));
            MacroKey.Add(new KeyValuePair<int, string>(5, "Six"));
            MacroKey.Add(new KeyValuePair<int, string>(6, "Seven"));
            MacroKey.Add(new KeyValuePair<int, string>(7, "Eight"));
            MacroKey.Add(new KeyValuePair<int, string>(8, "Nine"));
        }
        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }
        private void WriteToFile()
        {
            using (StreamWriter writer = new StreamWriter("config.txt"))
            {
                for (int i = 0; i < macroPad.Count(); i++)
                {
                    writer.WriteLine("{");
                    writer.WriteLine(macroPad[i].GetLayerName());
                    for (int j = 0; j < 9; j++)
                    {
                        writer.WriteLine(macroPad[i].GetButtonName(j));
                        writer.WriteLine(macroPad[i].GetButtonCommand(j));
                    }
                    writer.WriteLine("}");
                }
            }
        }
        private void ReadFromFile()
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.ShowDialog();
            var result = ofd.FileName;
            macroPad.Clear();
            MacroLayer layer = new MacroLayer();
            using (StreamReader reader = new StreamReader(result))
            {
                while (reader.Peek() >= 0)
                {
                    string line = reader.ReadLine();
                    if (line == "{")//New Macolayer
                    {

                        layer.SetLayerName(reader.ReadLine());
                        for (int i = 0; i < 9; i++)
                        {
                            layer.SetButtonName(i, reader.ReadLine());
                            layer.SetButtonCommand(i, reader.ReadLine());
                        }
                    }
                    if (line == "}")
                    {
                        macroPad.Add(layer);
                        layer = new MacroLayer();
                    }
                }
            }
        }
        //int 0 = prev int 1 = next
        private void PrevNext(int boolPrevNext)
        {
            if (boolPrevNext == 0)
            {
                if (currentLayer == 0) { } //Top layer
                else if (currentLayer != 0)
                {
                    currentLayer = currentLayer - 1;
                }
            }
            if (boolPrevNext == 1)
            {
                if (currentLayer == macroPad.Count() - 1) { } //Bottom Layer
                else { currentLayer = currentLayer + 1; }
            }
            UpdateScreen();
        }
        private void UpdateLayerName()
        {
            macroPad[currentLayer].SetLayerName(txtSetLayerName.Text);
            txtVisPadDisplay.Text = macroPad[currentLayer].GetLayerName();
            txtSetLayerName.Text = "";
        }
        private void UpdateButtonLabel(int index) 
        {
            lblSelectedButton.Text = "Selected Button: " + MacroKey[index];
            currentButton = index;
            lblSelectedButtonName.Text = "Button Name: " + macroPad[currentLayer].GetButtonName(index);
            lblSelectedButtonOperation.Text = "Button Operation: " + macroPad[currentLayer].GetButtonCommand(index);
        }
        private void UpdateButton()
        {
            macroPad[currentLayer].SetButtonName(currentButton, txtButtonName.Text);
            macroPad[currentLayer].SetButtonCommand(currentButton, txtNewButtonCommand.Text);
            UpdateScreen();
        }
        private void btnNewLayer_Click(object sender, EventArgs e)
        {
            MacroLayer ml = new MacroLayer();
            ml.SetUpDefaultButtons(MacroKey);
            macroPad.Add(ml);
            PrevNext(1);
        }
        private void btnSetLayername_Click(object sender, EventArgs e) { UpdateLayerName(); }
        private void btnPrev_Click(object sender, EventArgs e) { PrevNext(0); }
        private void btnNext_Click(object sender, EventArgs e) { PrevNext(1); }
        private void btnOne_Click(object sender, EventArgs e) { UpdateButtonLabel(0); }
        private void btnTwo_Click(object sender, EventArgs e) { UpdateButtonLabel(1); }
        private void btnThree_Click(object sender, EventArgs e) { UpdateButtonLabel(2); }
        private void btnFour_Click(object sender, EventArgs e) { UpdateButtonLabel(3); }
        private void btnFive_Click(object sender, EventArgs e) { UpdateButtonLabel( 4); }
        private void btnSix_Click(object sender, EventArgs e) { UpdateButtonLabel(5); }
        private void btnSeven_Click(object sender, EventArgs e) { UpdateButtonLabel(6); }
        private void btnEight_Click(object sender, EventArgs e) { UpdateButtonLabel(7); }
        private void btnNine_Click(object sender, EventArgs e) { UpdateButtonLabel( 8); }

        private void btnSetButton_Click(object sender, EventArgs e){ UpdateButton(); }

        private void button1_Click(object sender, EventArgs e)
        {
            lbxButtonOptions.ClearSelected();
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            WriteToFile();
        }

        private void btnLoadConfig_Click(object sender, EventArgs e)
        {
            ReadFromFile();
            currentLayer = 0;
            UpdateScreen();
        }
    }

    public class MacroLayer
    {
        private string layerName = "";
        private List<Button> buttonCommands = new List<Button>();

        public MacroLayer()
        {
            layerName = "";
            for (int i = 0; i < 9; i++)
            {
                Button b = new Button();
                buttonCommands.Add(b);
            }
        }

        public void SetUpDefaultButtons(IDictionary<int, string> MacroKey)
        {
            for (int i = 0; i < buttonCommands.Count(); i++)
            {
                buttonCommands[i].SetButtonName(MacroKey[i]);
                buttonCommands[i].SetButtonCommand("No Data");
            }
        }

        public void SetLayerName(string newName) { layerName = newName; }
        public string GetLayerName() { return layerName; }

        public void SetButtonName(int button, string name) { buttonCommands[button].SetButtonName(name); }
        public void SetButtonCommand(int button, string command) { buttonCommands[button].SetButtonCommand(command); }

        public string GetButtonName(int button) { return buttonCommands[button].GetButtonName(); }
        public string GetButtonCommand(int button) { return buttonCommands[button].GetButtonOparation(); }
    }

    public class Button
    {
        private string buttonName;
        private string buttonOperation;
        public Button() 
        {
            buttonName = "";
            buttonOperation = "";
        }

        public void SetButtonName(string name) { buttonName = name; }
        public void SetButtonCommand(string command) { buttonOperation = command; }

        public string GetButtonName() { return buttonName; }
        public string GetButtonOparation() { return buttonOperation; }

        internal void SetButtonName(object macroKey)
        {
            throw new NotImplementedException();
        }
    }
}
