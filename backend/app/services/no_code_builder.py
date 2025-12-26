from typing import Dict, List, Optional
import uuid
from datetime import datetime


class NoCodeBuilderService:
    """Service for generating tools from natural language descriptions"""
    
    def __init__(self):
        self.tools_storage = {}  # In production, use database
    
    async def generate_tool(
        self,
        description: str,
        tool_type: Optional[str] = None,
        user_id: int = None
    ) -> Dict:
        """Generate a tool from natural language description"""
        tool_id = str(uuid.uuid4())
        
        # Analyze description to determine tool type
        if not tool_type:
            tool_type = self._detect_tool_type(description)
        
        # Generate code based on description
        code = self._generate_code(description, tool_type)
        
        tool = {
            "tool_id": tool_id,
            "name": self._extract_tool_name(description),
            "description": description,
            "tool_type": tool_type,
            "code": code,
            "preview": self._generate_preview(code),
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Store tool
        self.tools_storage[tool_id] = tool
        
        return tool
    
    def _detect_tool_type(self, description: str) -> str:
        """Detect tool type from description"""
        description_lower = description.lower()
        
        if any(kw in description_lower for kw in ["ad", "advertisement", "marketing"]):
            return "ad_generator"
        elif any(kw in description_lower for kw in ["stage", "staging", "virtual"]):
            return "digital_staging"
        elif any(kw in description_lower for kw in ["calculator", "calculate", "compute"]):
            return "calculator"
        elif any(kw in description_lower for kw in ["form", "input", "collect"]):
            return "form_builder"
        else:
            return "custom"
    
    def _extract_tool_name(self, description: str) -> str:
        """Extract tool name from description"""
        # Simple extraction - in production, use NLP
        words = description.split()[:5]
        return " ".join(words).title()
    
    def _generate_code(self, description: str, tool_type: str) -> str:
        """Generate code based on description and type"""
        if tool_type == "ad_generator":
            return self._generate_ad_generator_code(description)
        elif tool_type == "digital_staging":
            return self._generate_staging_code(description)
        elif tool_type == "calculator":
            return self._generate_calculator_code(description)
        elif tool_type == "form_builder":
            return self._generate_form_code(description)
        else:
            return self._generate_custom_code(description)
    
    def _generate_ad_generator_code(self, description: str) -> str:
        """Generate ad generator code"""
        return """
import React from 'react';

function AdGenerator() {
    const [propertyData, setPropertyData] = React.useState({
        address: '',
        price: '',
        bedrooms: '',
        bathrooms: ''
    });
    
    const generateAd = () => {
        return `""" + description + """
        
Property Details:
- Address: ${propertyData.address}
- Price: ${propertyData.price}
- Bedrooms: ${propertyData.bedrooms}
- Bathrooms: ${propertyData.bathrooms}`;
    };
    
    return (
        <div className="ad-generator">
            <h2>Ad Generator</h2>
            <input 
                placeholder="Address" 
                value={propertyData.address}
                onChange={(e) => setPropertyData({...propertyData, address: e.target.value})}
            />
            <button onClick={generateAd}>Generate Ad</button>
        </div>
    );
}

export default AdGenerator;
"""
    
    def _generate_staging_code(self, description: str) -> str:
        """Generate digital staging code"""
        return """
import React from 'react';

function DigitalStaging() {
    const [image, setImage] = React.useState(null);
    
    const stageRoom = async () => {
        // AI-powered staging logic
        console.log('Staging room based on: """ + description + """');
    };
    
    return (
        <div className="digital-staging">
            <h2>Digital Staging</h2>
            <input type="file" onChange={(e) => setImage(e.target.files[0])} />
            <button onClick={stageRoom}>Stage Room</button>
        </div>
    );
}

export default DigitalStaging;
"""
    
    def _generate_calculator_code(self, description: str) -> str:
        """Generate calculator code"""
        return """
import React, { useState } from 'react';

function Calculator() {
    const [inputs, setInputs] = useState({});
    const [result, setResult] = useState(0);
    
    const calculate = () => {
        // Calculation logic based on: """ + description + """
        setResult(0);
    };
    
    return (
        <div className="calculator">
            <h2>Calculator</h2>
            <button onClick={calculate}>Calculate</button>
            <div>Result: {result}</div>
        </div>
    );
}

export default Calculator;
"""
    
    def _generate_form_code(self, description: str) -> str:
        """Generate form builder code"""
        return """
import React, { useState } from 'react';

function CustomForm() {
    const [formData, setFormData] = useState({});
    
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Form submitted:', formData);
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <h2>Custom Form</h2>
            <p>""" + description + """</p>
            <button type="submit">Submit</button>
        </form>
    );
}

export default CustomForm;
"""
    
    def _generate_custom_code(self, description: str) -> str:
        """Generate custom code"""
        return """
import React from 'react';

function CustomTool() {
    return (
        <div className="custom-tool">
            <h2>Custom Tool</h2>
            <p>""" + description + """</p>
            <p>This tool was generated from your description.</p>
        </div>
    );
}

export default CustomTool;
"""
    
    def _generate_preview(self, code: str) -> str:
        """Generate preview of the code"""
        # Extract key components for preview
        return code[:200] + "..." if len(code) > 200 else code
    
    async def list_user_tools(self, user_id: int) -> List[Dict]:
        """List all tools for a user"""
        return [
            tool for tool in self.tools_storage.values()
            if tool.get("user_id") == user_id
        ]
    
    async def get_tool(self, tool_id: str, user_id: int) -> Optional[Dict]:
        """Get a specific tool"""
        tool = self.tools_storage.get(tool_id)
        if tool and tool.get("user_id") == user_id:
            return tool
        return None

