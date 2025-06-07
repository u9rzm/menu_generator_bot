import os
import aiohttp
from typing import Optional
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ...application.use_cases.manage_image import ManageImageUseCase
from ...domain.models.image_management import ImageType
from ...domain.exceptions import DomainException
from .base_handler import BaseHandler
from .logging.logger import Logger
from .keyboards.organization_keyboard import get_back_to_org_buttons

class ImageHandler(BaseHandler):
    """Handler for image-related operations"""
    
    def __init__(self, bot: Bot, dp: Dispatcher, image_use_case: ManageImageUseCase, logger: Logger):
        self.image_use_case = image_use_case
        super().__init__(bot, dp)
        self.logger = logger
        self.api_url = os.getenv("API_URL")
        self.images_url = os.getenv("IMAGES_URL")

    def _register_handlers(self) -> None:
        """Register message and callback handlers"""
        self.dp.message.register(self.handle_upload_image, Command("upload_image"))
        self.dp.message.register(self.handle_get_image, Command("get_image"))
        self.dp.message.register(self.handle_delete_image, Command("delete_image"))
        self.dp.callback_query.register(self.handle_image_callback, lambda c: c.data.startswith("image_"))

    async def handle_upload_image(self, callback_query: CallbackQuery, state: FSMContext):
        """Handle image upload request"""
        org_id = int(callback_query.data.split("_")[2])
        image_type = callback_query.data.split("_")[3]
        
        # Store organization ID and image type in state
        await state.update_data(org_id=org_id, image_type=image_type)
        
        await callback_query.message.answer(
            f"📸 Пожалуйста, отправьте изображение для {image_type}.\n"
            "Поддерживаемые форматы: JPG, PNG, GIF"
        )
        
    async def handle_image_received(self, message: Message, state: FSMContext):
        """Handle received image"""
        if not message.photo:
            await message.answer(
                "❌ Пожалуйста, отправьте изображение в формате JPG, PNG или GIF."
            )
            return
            
        data = await state.get_data()
        org_id = data.get('org_id')
        image_type = data.get('image_type')
        
        if not org_id or not image_type:
            await message.answer(
                "❌ Произошла ошибка. Пожалуйста, попробуйте снова."
            )
            return
            
        try:
            # Get the largest photo
            photo = message.photo[-1]
            file_id = photo.file_id
            file = await self.bot.get_file(file_id)
            file_path = f"temp_{file_id}.jpg"
            
            # Download file
            await self.bot.download_file(file.file_path, file_path)
            
            # Upload to API
            async with aiohttp.ClientSession() as session:
                with open(file_path, 'rb') as f:
                    form = aiohttp.FormData()
                    form.add_field('file', f, filename=f"{image_type}.jpg")
                    form.add_field('image_type', image_type)
                    
                    async with session.post(
                        f"{self.api_url}/organizations/{org_id}/images",
                        data=form
                    ) as resp:
                        if resp.status != 200:
                            raise Exception(f"Failed to upload image: {await resp.text()}")
                        image_data = await resp.json()
                        
            # Delete temporary file
            os.remove(file_path)
            
            await message.answer(
                "✅ Изображение успешно загружено!",
                reply_markup=get_back_to_org_buttons(org_id)
            )
            
            # Clear state
            await state.clear()
            
        except Exception as e:
            self.logger.error(f"Error uploading image: {str(e)}")
            await message.answer(
                "❌ Произошла ошибка при загрузке изображения. Пожалуйста, попробуйте позже."
            )

    async def handle_get_image(self, message: Message) -> None:
        """Handle get image command"""
        try:
            # Parse command arguments
            args = message.text.split()[1:]
            if len(args) != 1:
                await message.answer("Использование: /get_image <тип>")
                return

            image_type = args[0]

            # Validate image type
            try:
                image_type = ImageType(image_type)
            except ValueError:
                await message.answer(f"Неверный тип изображения. Доступные типы: {', '.join(t.value for t in ImageType)}")
                return

            # Get image
            image = await self.image_use_case.get_image(
                organization_id=message.from_user.id,
                image_type=image_type
            )

            if not image:
                await message.answer("Изображение не найдено")
                return

            # Send image
            await message.answer_photo(
                photo=image.file_path,
                caption=f"Тип: {image.image_type.value}\nЗагружено: {image.uploaded_at}"
            )

        except DomainException as e:
            await self._handle_domain_exception(message, e)
        except Exception as e:
            await message.answer("Произошла ошибка при получении изображения")

    async def handle_delete_image(self, callback_query: CallbackQuery):
        """Delete image"""
        _, _, org_id, image_id = callback_query.data.split("_")
        org_id = int(org_id)
        image_id = int(image_id)
        
        try:
            async with aiohttp.ClientSession() as session:
                # Delete image
                async with session.delete(f"{self.api_url}/organizations/{org_id}/images/{image_id}") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to delete image: {await resp.text()}")
                        
                await callback_query.message.answer(
                    "✅ Изображение успешно удалено!",
                    reply_markup=get_back_to_org_buttons(org_id)
                )
                
        except Exception as e:
            self.logger.error(f"Error deleting image: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при удалении изображения. Пожалуйста, попробуйте позже."
            )

    async def handle_image_callback(self, callback: CallbackQuery) -> None:
        """Handle image-related callback queries"""
        try:
            # Parse callback data
            data = callback.data.split("_")
            if len(data) < 3:
                await callback.answer("Неверный формат данных")
                return

            action = data[1]
            image_type = data[2]

            # Validate image type
            try:
                image_type = ImageType(image_type)
            except ValueError:
                await callback.answer("Неверный тип изображения")
                return

            if action == "delete":
                success = await self.image_use_case.delete_image(
                    organization_id=callback.from_user.id,
                    image_type=image_type
                )
                if success:
                    await callback.message.edit_text("Изображение успешно удалено")
                else:
                    await callback.message.edit_text("Изображение не найдено")

            elif action == "get":
                image = await self.image_use_case.get_image(
                    organization_id=callback.from_user.id,
                    image_type=image_type
                )
                if image:
                    await callback.message.answer_photo(
                        photo=image.file_path,
                        caption=f"Тип: {image.image_type.value}\nЗагружено: {image.uploaded_at}"
                    )
                else:
                    await callback.message.edit_text("Изображение не найдено")

        except DomainException as e:
            await self._handle_callback_domain_exception(callback, e)
        except Exception as e:
            await callback.answer("Произошла ошибка при обработке запроса")

    async def handle_show_images(self, callback_query: CallbackQuery):
        """Show organization images"""
        org_id = int(callback_query.data.split("_")[2])
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get organization images
                async with session.get(f"{self.api_url}/organizations/{org_id}/images") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get images: {await resp.text()}")
                    images = await resp.json()
                    
                    if not images:
                        await callback_query.message.answer(
                            "❌ Нет загруженных изображений",
                            reply_markup=get_back_to_org_buttons(org_id)
                        )
                        return
                        
                # Create keyboard with image options
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(
                            text=f"📸 {image['image_type']}",
                            callback_data=f"show_image_{org_id}_{image['id']}"
                        )]
                        for image in images
                    ] + [[InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]]
                )
                
                await callback_query.message.answer(
                    "📸 Выберите изображение для просмотра:",
                    reply_markup=keyboard
                )
                
        except Exception as e:
            self.logger.error(f"Error showing images: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при загрузке изображений. Пожалуйста, попробуйте позже."
            )
            
    async def handle_show_image(self, callback_query: CallbackQuery):
        """Show specific image"""
        _, _, org_id, image_id = callback_query.data.split("_")
        org_id = int(org_id)
        image_id = int(image_id)
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get image details
                async with session.get(f"{self.api_url}/organizations/{org_id}/images/{image_id}") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get image: {await resp.text()}")
                    image = await resp.json()
                    
                # Create keyboard with image options
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_image_{org_id}_{image_id}")],
                        [InlineKeyboardButton(text="◀️ Назад к изображениям", callback_data=f"show_images_{org_id}")]
                    ]
                )
                
                await callback_query.message.answer_photo(
                    photo=f"{self.images_url}/{image['file_path']}",
                    caption=f"📸 {image['image_type']}\n{image.get('description', '')}",
                    reply_markup=keyboard
                )
                
        except Exception as e:
            self.logger.error(f"Error showing image: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при загрузке изображения. Пожалуйста, попробуйте позже."
            ) 