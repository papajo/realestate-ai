from fastapi import WebSocket, WebSocketDisconnect, Query
from app.websocket.manager import websocket_manager
from app.core.security import decode_token
from jose import JWTError


async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    """WebSocket endpoint for real-time notifications"""
    try:
        # Decode token to get user_id
        payload = decode_token(token)
        if not payload:
            await websocket.close(code=1008, reason="Invalid token")
            return
        
        user_id = payload.get("user_id")
        if not user_id:
            await websocket.close(code=1008, reason="Invalid token")
            return
        
        await websocket_manager.connect(websocket, user_id)
        
        try:
            while True:
                data = await websocket.receive_text()
                # Echo back or process message
                await websocket_manager.send_personal_message(
                    {"message": f"Received: {data}"},
                    websocket
                )
        except WebSocketDisconnect:
            websocket_manager.disconnect(websocket, user_id)
    except Exception as e:
        await websocket.close(code=1011, reason=f"Error: {str(e)}")

