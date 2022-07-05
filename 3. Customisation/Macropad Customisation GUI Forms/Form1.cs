using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Macropad_Customisation_GUI_Forms
{
    public partial class Form1 : Form
    {
        List<MacroLayer> macroPad = new List<MacroLayer>();
        string existingMacroPadLayout = "";
        string macropadFileLocation = "";
        int currentLayer = 0;
        int currentButton = 0;
        IDictionary<int, string> MacroKey = new Dictionary<int, string>();
        public Form1()
        {
            InitializeComponent();
            InitialiseKey();
            MacroLayer ml = new MacroLayer();
            macroPad.Add(ml);
            //connectedMacroPad();
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
        private void connectedMacroPad() //Will create or get the location of a config file
        {
            //Read from file
            string message = "Is there a macropad connected?";
            const string caption = "Select message macropad";
            var result = MessageBox.Show(message, caption, MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (result == DialogResult.Yes) { GetMacroLocation(); }
            else { macropadFileLocation = ""; }

        }
        private void GetMacroLocation()
        {
            MessageBox.Show("Please select the file inside the connected macropad called: \nConfig.txt");
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {
                    macropadFileLocation = openFileDialog.FileName;
                }
            }
        }

        //int 0 = prev int 1 = next
        private void UpdateMacroPadDisplay(int boolPrevNext)
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
            txtVisPadDisplay.Text = macroPad[currentLayer].GetLayerName();
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
        }

        private void btnNewLayer_Click(object sender, EventArgs e)
        {
            MacroLayer ml = new MacroLayer();
            macroPad.Add(ml);
            UpdateMacroPadDisplay(1);
        }
        private void btnSetLayername_Click(object sender, EventArgs e) { UpdateLayerName(); }
        private void btnPrev_Click(object sender, EventArgs e) { UpdateMacroPadDisplay(0); }
        private void btnNext_Click(object sender, EventArgs e) { UpdateMacroPadDisplay(1); }



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
        public MacroLayer(int id, string name, List<Button> commands)
        {
            layerName = name;
            buttonCommands = commands;
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


    }
}
